import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import preprocessor, helper
from matplotlib.font_manager import FontProperties
import emoji
import seaborn as sns
# Bengali font problem solving
font_path = './shorif.ttf'
bengali_font = FontProperties(fname=font_path)







st.sidebar.title('Whats App Chat Analyzer')
upload_file = st.sidebar.file_uploader('Choose a file')
if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode('utf-8')
    #st.text(data)
    df = preprocessor.preprocess(data)


    # fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button('Show Analysis'):
        title = 'Showing analysis for: '+ selected_user;
        st.title(title)
        new_df, num_messages, words, media_num, links = helper.fetch_stats(selected_user, df)
        st.dataframe(new_df)
        col1, col2, col3, col4 = st.columns(4)


        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Total Media')
            st.title(media_num)
        with col4:
            st.header('Total Links')
            st.title(links)
        # finding the busiest user
        if selected_user == 'Overall':
            x, percent = helper.stats(df)
            st.title('Most Busy User')
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(percent)

        df_wc = helper.create_word_cloud(selected_user, df)
        st.title('WrodCloud')
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

         # most common word
        st.title('Most Common Words')
        most_common_words = helper.most_common_word(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(most_common_words[0], most_common_words[1])
        ax.set_title('Most Common Word', fontproperties=bengali_font)
        ax.set_xlabel('Word', fontproperties=bengali_font)
        ax.set_ylabel('Frequency', fontproperties=bengali_font)
        ax.set_xticklabels(most_common_words[0], fontproperties=bengali_font)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji analysis
        emoji_df = helper.emoji_num(selected_user, df)
        st.title("Emoji Analysis")
        if emoji_df.empty:
            st.text("Opps! --- No emoji found ---")
        else:
            emoji_num = 'Total emoji: '+ str(len(emoji_df[0]))
            st.text(emoji_num)
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                labels = [emoji.emojize(x, use_aliases=True) for x in emoji_df[0]]
                ax.pie(emoji_df[1], labels=labels)
                st.pyplot(fig)

        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, df)

        fig, ax = plt.subplots()
        ax.bar(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title('Daily Timeline')
        dailytimeline = helper.dailytimeline(selected_user, df)
        fig, ax = plt.subplots()

        ax.plot(dailytimeline['only_date'], dailytimeline['message'],color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most Active Day')
            active_day = helper.active_day(selected_user, df)
            fig, ax = plt.subplots()

            ax.bar(active_day.index, active_day.values, color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Active Month")
            active_month = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()

            ax.bar(active_month.index, active_month.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        st.title('Most Busy Time')
        activity_heat = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_heat)
        st.pyplot(fig)


