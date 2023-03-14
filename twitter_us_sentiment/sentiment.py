#Sentiment analysis of US Airlines tweets
#By TUSHAR AGGARWAL
#github.com/tushar2704



#Importing the required packages
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import gdown
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


#Hiding right menu
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

#setting titles
st.title("🐥✈️U.S. Airlines Tweet's Sentiment Analysis")
st.markdown("### By Tushar Aggarwal")

#Loading and checking data
url = "https://drive.google.com/uc?id=1xa5hgmjpzcjrZ2B_FyREvQ4gQxB2srkM"
output = "Tweets.csv" # replace with the name you want for your CSV file
gdown.download(url, output, quiet=False)

#def load_data
@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv(output)
    data['tweet_created']=pd.to_datetime(data['tweet_created'])
    return data

df=load_data()


#Sidebar for random tweeets selection
st.sidebar.subheader("Show random tweet")
random_tweet =st.sidebar.radio('Select sentiment type:',('positive', 'neutral','negative'))
st.sidebar.markdown(df.query('airline_sentiment== @random_tweet')[["text"]].sample(n=1).iat[0,0])
st.sidebar.markdown("_______________")

#Sidebar for total no of tweets with chart type selection
st.sidebar.markdown("### No. of tweets by sentiment")
select =st.sidebar.selectbox("Visualiztion type",['Histogram', 'Pie Chart'], key='1')
sentiment_count = df['airline_sentiment'].value_counts()
sentiment_count =pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

#checkbox to hide plots
if not st.sidebar.checkbox("Hide", True):
    st.markdown("### No. of Tweets by Sentiment")
    if select =='Histogram':
        fig =px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig=px.pie(sentiment_count, values='Tweets',names='Sentiment')
        st.plotly_chart(fig)

#interactive map
st.sidebar.markdown("_______________")
st.sidebar.subheader("When and from where users are tweeting from ?")
hour = st.sidebar.slider("Hour of day", 0,23)
modified_data = df[df['tweet_created'].dt.hour==hour]
if not st.sidebar.checkbox("Closed", True, key='2'):
    st.markdown("### Tweets location based on time of the day")
    st.markdown("%i tweets between %i:00 and %i:00" %(len(modified_data), hour,(hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

#Tweets by Airline
st.sidebar.markdown("_______________")
st.sidebar.subheader("Airlines tweets by sentiment")
choice =st.sidebar.multiselect("Pick the Airline",("US Airways", "United", "American", "SouthWest", "Delta", "Virgin America"), key='3')

if len(choice)>0:
    choice_data =df[df['airline'].isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline',y='airline_sentiment', histfunc='count', color='airline_sentiment',
                              facet_col='airline_sentiment', labels={'airline_sentiments':'tweets'},
                              height=600, width=800)
    st.plotly_chart(fig_choice)

#Wordcloud
st.sidebar.markdown("_______________")
st.sidebar.subheader("WordCloud")
word_sentiment = st.sidebar.radio("Displacy WordCloud for:", ("positive",'negative', 'neutral'))

if not st.sidebar.checkbox("Close", True, key='4'):
    st.subheader("WordCloud for %s sentiment"%(word_sentiment))
    df_1= df[df['airline_sentiment']==word_sentiment]
    words = " ".join(df_1['text'])
    process_word = ' '.join( [word for word in words.split() if "http" not in word and not word.startswith("@") and word !="RT"])
    wordcloud =WordCloud(stopwords =STOPWORDS, background_color='white').generate(process_word)
  
    st.pyplot(wordcloud)

st.sidebar.markdown("_______________")


































































