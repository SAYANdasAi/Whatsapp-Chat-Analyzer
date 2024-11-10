from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(user_name,df):

    if user_name != 'Overall':
        df = df[df['users'] == user_name]
    # fetch number of messages
    num_messages = df.shape[0]

    # fetch number of words

    words = []  
    for message in df['messages']:
        words.extend(message.split())

    # fetch number of media files

    num_media = df[df['messages']=='<Media omitted>'].shape[0]

    # fetch number of links
    extract = URLExtract()
    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media,len(links)

def busiest_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','users':'percent'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users']!='group_notification']
    temp = temp[temp['messages']!='<Media omitted>']
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            words.append(word)
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

def most_used_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users']!='group_notification']
    temp = temp[temp['messages']!='<Media omitted>']
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            words.append(word)

    word_count = pd.DataFrame(Counter(words).most_common(20))

    return word_count

def most_used_emojis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(20))
    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    
    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    return df.pivot_table(index='day_name',columns='period',values='messages',aggfunc='count').fillna(0)

