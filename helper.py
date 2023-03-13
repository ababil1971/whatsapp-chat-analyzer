from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user, df):
    word = []
    links = []
    extractor = URLExtract()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    for message in df['message']:
        links.extend(extractor.find_urls(message))
        word.extend(message.split())


    # fetch the media number
    media_num = df[df['message'] == '<Media omitted>\n'].shape[0]

    return df, df.shape[0], len(word), media_num, len(links)


def stats(df):
    x = df['user'].value_counts().head()
    df_pie = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df_pie
def create_word_cloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    font_path = './shorif.ttf'
    wc = WordCloud(font_path= font_path,width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=' '))
    print(df_wc)
    return df_wc

def most_common_word(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>\n']
    f = open('./stopword.txt', 'r')
    stop_word = f.read()

    words = []
    for message in df['message']:
        for word in message.lower().split():
            if word not in stop_word:
                words.append(word)

    new_df = pd.DataFrame(Counter(words).most_common(20))
    return new_df

def emoji_num(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([x for x in message if x in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline


def dailytimeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()

    return daily_timeline

def active_day(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    active_num = df['day_name'].value_counts()
    return active_num
def month_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    active_months = df['month'].value_counts()
    return active_months

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    activity_heat = df.pivot_table(index='day_name',columns='period', values='message',aggfunc='count').fillna(0)
    return activity_heat