from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import re
import emoji
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# print(final_comments)

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))


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


df = pd.read_csv("UScomments.csv", usecols=[1], nrows=40000)


df.iloc[:, 0] = df.iloc[:, 0].apply(lambda text: text_processing(str(text)))


comment_list = df.iloc[:, 0].tolist()



def sentiment_score (comment,polarity):
    vader_sentiment=SentimentIntensityAnalyzer()

    if not isinstance(comment, str):
        comment = str(comment)

    sentiment_score=vader_sentiment.polarity_scores(comment)['compound']
    # polarity.append(sentiment_score)
    if sentiment_score > 0.05:
        polarity.append(1)
    elif sentiment_score< -0.05:
        polarity.append(-1)
    else:
        polarity.append(0)

polarity=[]


for comment in comment_list:
   sentiment_score(comment,polarity)


df = pd.DataFrame({'comment': comment_list, 'polarity': polarity})


df.to_csv('youtube_comments.csv', index=False)

df['comment'] = df['comment'].fillna('')

print('YOUR 40K POLARITY LABELLING DONE IN youtube_comments.csv')