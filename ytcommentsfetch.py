from googleapiclient.discovery import build 
import re 
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

api_key='AIzaSyAv_gclaUtkEUlArmiKwaG1fz9UCuHOuVE'

youtube = build('youtube', 'v3', developerKey=api_key)

video_id=input("Enter video url")[-11:]

video_response = youtube.videos().list(
    part='snippet',
    id=video_id
).execute()


video_snippet = video_response['items'][0]['snippet']
uploader_channel_id = video_snippet['channelId']

comments=[]


nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()



nextPageToken = None

while len(comments) < 1000:
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100,
        pageToken=nextPageToken
    )
    response = request.execute()
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        if comment['authorChannelId']['value'] != uploader_channel_id:
            comments.append(comment['textDisplay'])
    nextPageToken = response.get('nextPageToken')

    if not nextPageToken:
        break   

threshold_ratio=0.65

final_comments=[]

hyperlink_pattern = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

for comment_text in comments:

    comment_text = comment_text.lower().strip()

    emojis = emoji.emoji_count(comment_text)
    text_characters = len(re.sub(r'\s', '', comment_text))

    if hyperlink_pattern.search(comment_text):  
        continue


    emojis = emoji.emoji_count(comment_text)  
    text_characters = len(re.sub(r'\s', '', comment_text)) 


    words = comment_text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    cleaned_text = ' '.join(words)

    if any(char.isalnum() for char in cleaned_text):  
        if emojis == 0 or (text_characters - emojis / text_characters) > threshold_ratio:
            final_comments.append(cleaned_text)


# print(final_comments)

def sentiment_score (comment,polarity):
    vader_sentiment=SentimentIntensityAnalyzer()
    sentiment_score=vader_sentiment.polarity_scores(comment)['compound']
    # polarity.append(sentiment_score)
    if sentiment_score > 0.01:
        polarity.append(1)
    elif sentiment_score< -0.01:
        polarity.append(-1)
    else:
        polarity.append(0)

polarity=[]


for comment in final_comments:
   sentiment_score(comment,polarity)


# print(polarity)

df = pd.DataFrame({'comment': final_comments, 'polarity': polarity})

df.to_csv('youtube_comments.csv', index=False)

print(df)


vectorizer = TfidfVectorizer(max_features=5000) 
X = vectorizer.fit_transform(df['comment']).toarray()
y = df['polarity']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Predict on test data
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Random Forest Accuracy: {accuracy:.2f}")
