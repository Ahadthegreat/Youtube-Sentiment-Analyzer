from googleapiclient.discovery import build 
import re 
import matplotlib.pyplot as plt
import emoji
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


api_key='AIzaSyAv_gclaUtkEUlArmiKwaG1fz9UCuHOuVE'

youtube = build('youtube', 'v3', developerKey=api_key)

video_id=input("Enter video url :")[-11:]

video_response = youtube.videos().list(
    part='snippet',
    id=video_id
).execute()


video_snippet = video_response['items'][0]['snippet']
uploader_channel_id = video_snippet['channelId']

comments=[]


nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))


nextPageToken = None

#Fetching 1K comments for analysis in comment

while len(comments) < 10000:
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


final_comments=[]

hyperlink_pattern = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')



def text_processing(text):   
    # convert text into lowercase
    text = text.lower()

    # remove new line characters in text
    text = re.sub(r'\n',' ', text)
    
    # remove punctuations from text
    text = re.sub('[%s]' % re.escape(string.punctuation), "", text)
    
    # remove references and hashtags from text
    text = re.sub("^a-zA-Z0-9$,.", "", text)
    
    # remove multiple spaces from text
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    
    # remove special characters from text
    text = re.sub(r'\W', ' ', text)
    
    emoji.demojize(text)

    text = ' '.join([word for word in word_tokenize(text) if word not in stop_words])

    return text

 #Comment pre proccessing 

for comment_text in comments:

    if hyperlink_pattern.search(comment_text):  
        continue

    comment_text=text_processing(comment_text)

    final_comments.append(comment_text)


print(final_comments)



df=pd.read_csv('youtube_comments.csv')

vectorizer = TfidfVectorizer(max_features=5000,  binary=True, ngram_range=(1, 3),  sublinear_tf=True)

df['comment'] = df['comment'].fillna('')


X = vectorizer.fit_transform(df['comment']).toarray()
y = df['polarity']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=30)




from sklearn.linear_model import SGDClassifier

sgd = SGDClassifier(loss='hinge', random_state=42)
sgd.fit(X_train, y_train)
y_pred_sgd = sgd.predict(X_test)
print(f"SGD Classifier Accuracy: {accuracy_score(y_test, y_pred_sgd):.5f}")

final_comment_predict=sgd.predict(vectorizer.transform(final_comments))

pos_comm=0
neg_comm=0
neut_comm=0

for i in final_comment_predict:
    if i == -1:
        neg_comm=neg_comm+1 
    elif i==0:
        neut_comm=neut_comm+1
    else:
        pos_comm=pos_comm+1


print(str(pos_comm)+" "+str(neg_comm)+" "+str(neut_comm))


labels = ['Positive', 'Negative', 'Neutral']
values = [pos_comm, neg_comm, neut_comm]
plt.bar(labels, values, color=['green', 'red', 'gray'])
plt.title('YouTube Comment Sentiment Distribution')
plt.show()


# httwatch?v=aDF_ESN80r8