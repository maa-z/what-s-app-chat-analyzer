import streamlit as st
from preprocessor import preprocessor,fetch_stats,most_busy_user,most_common_words,get_monthly_timeline,get_daily_timeline,get_day_timeline
# from preprocessor import create_word_cloud
from matplotlib import pyplot as plt


st.sidebar.title("What's App Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor(data)
    # st.dataframe(df)
    st.title("Top Statistics")
    ## unique user

    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"OverAll")
    selected_user = st.sidebar.selectbox("Show Analysis WRT",user_list)
    if st.sidebar.button("Show Analysis"):
        
        col1 , col2 , col3  = st.columns(3)
        num_messages,words,num_media_messages = fetch_stats(selected_user,df)
        with col1:
            st.header("Messages")
            st.title(num_messages)
        with col2:
            st.header("Words")
            st.title(words)
        with col3:
            st.header("Media")
            st.title(num_media_messages)
        # with col2:
        #     st.header("Total Words")
        #     st.title(words)

        # finding the busiest users in the group(Group level)
        if selected_user == "OverAll":
            st.title('Most Busy Users')
            x , new_df = most_busy_user(df)
            fig , ax = plt.subplots()
            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        # df_wc = create_word_cloud(selected_user,df)
        # fig , ax = plt.subplots()
        # ax.imshow(df_wc)
        # st.pyplot(fig)


        most_common_words = most_common_words(selected_user,df)
        fig , ax = plt.subplots()
        ax.barh(most_common_words[0],most_common_words[1],color="orange")
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)

        # monthly time
        st.title("Total Messages Per Month")
        timeline = get_monthly_timeline(selected_user,df)
        fig , ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color="green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily time
        st.title("Top Five Days With Most Messages")
        timeline = get_daily_timeline(selected_user,df)
        # st.dataframe(timeline)
        fig , ax = plt.subplots()
        ax.bar(timeline['message_date'].astype(str),timeline['message'],color="red")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # day time

        st.title("Day Wise Total Messages")
        timeline = get_day_timeline(selected_user,df)
        # st.dataframe(timeline)
        fig , ax = plt.subplots()
        ax.bar(timeline['message_date'].astype(str),timeline['message'],color="yellow")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)



            
    