import pandas as pd
import re
# from wordcloud import WordCloud
from collections import Counter 
# import matplotlib.pyplot as plt
# from urlextract import URLExtract
# urlextract
def fetch_message_user(text):
    p = ': '
    l = re.split(p,text)
    return pd.Series([l[0],l[1]])

def preprocessor(data):
    pattern_mess = '\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\u202f(am|pm)\s-\s'
    pattern_dates = '\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}'
    messages = re.split(pattern_mess,data)[1:]
    messages = messages[1::2]
    dates = re.findall(pattern_dates,data)
    df = pd.DataFrame({'user_message':messages,'message_date':dates})
    df = df.iloc[1:,:]
    df[['user','message']] = df['user_message'].apply(fetch_message_user)
    df['message_date'] = pd.to_datetime(df['message_date'],dayfirst=True,format="mixed")
    wapp = df[['message_date','user','message']]
    wapp['month'] = wapp['message_date'].dt.month_name()
    wapp['day'] = wapp['message_date'].dt.day
    wapp['hour'] = wapp['message_date'].dt.hour
    wapp['minute'] = wapp['message_date'].dt.minute
    wapp['year'] = wapp['message_date'].dt.year
    return wapp


def fetch_stats(selected_user,df):
    if selected_user!="OverAll":
        df = df[df['user']==selected_user]

    # 1. number of messages
    num_messages = df.shape[0]
    # 2. number of words
    words = 0
    for w in df['message']:
        words += len(w.split(" "))
    # 3. number of media 
    num_media_messages = df[df['message']=="<Media omitted>\n"].shape[0]
    # 4 . number of link
    
    return num_messages , words , num_media_messages


def most_busy_user(df):
    x = df['user'].value_counts()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x ,df

# def create_word_cloud(selected_user,df):
#     if selected_user!="OverAll":
#         df = df[df['user']==selected_user]
#     wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
#     df_wc = wc.generate(df['message'].str.cat(sep=" "))
#     return df_wc


def most_common_words(selected_user,df):
    if selected_user!="OverAll":
        df = df[df['user']==selected_user]
    f = open('stop_word_hinglish.txt','r')
    stop_words = f.read()
    words = []
    for message in df['message']:
        if message=='<Media omitted>\n':
            continue
        words.extend([i for i in message.lower().split(" ") if len(i)>2 and i not in stop_words and i!='null\n'])
    new_df = pd.DataFrame(Counter(words).most_common(20))
    return new_df


def get_monthly_timeline(selected_user,df):
    if selected_user!="OverAll":
        df = df[df['user']==selected_user]
    timeline = df.groupby(['year','month']).count()['message'].reset_index()
    t = []
    for i in range(timeline.shape[0]):
        t.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time'] = t
    return timeline


def get_daily_timeline(selected_user,df):
    if selected_user!="OverAll":
        df = df[df['user']==selected_user]
    messages_per_date = df.groupby(df['message_date'].dt.date)['message'].count().sort_values(ascending=False).reset_index().head(5)
    return messages_per_date

def get_day_timeline(selected_user,df):
    if selected_user!="OverAll":
        df = df[df['user']==selected_user]
    messages_per_day = df.groupby(df['message_date'].dt.day_name())['message'].count().sort_values(ascending=False).reset_index().head(5)
    return messages_per_day














