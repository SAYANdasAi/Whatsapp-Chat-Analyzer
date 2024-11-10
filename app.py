import streamlit as st
from preprocessor import preprocess
from helper import fetch_stats, busiest_users, create_wordcloud, most_used_words, most_used_emojis, monthly_timeline, daily_timeline, week_activity_map, month_activity_map, activity_heatmap
import matplotlib.pyplot as plt
import seaborn as sns

# Custom CSS for rounded corners, colors, and enhanced layout
st.markdown("""
    <style>
        /* General styling */
        body {
            font-family: 'Arial', sans-serif;
            color: #333;
            background-color: #f8f9fa;
        }

        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #3d5a80;
            color: #ffffff;
            padding: 20px;
            border-radius: 10px;
        }

        /* Title styling */
        h1, h2 {
            color: #3d5a80;
            font-weight: bold;
            text-align: center;
        }

        /* Container styling for better layout */
        .stContainer {
            padding: 10px;
            background-color: #edf2f4;
            border-radius: 10px;
            margin-top: 20px;
        }

        /* Rounded images */
        .stImage > img {
            border-radius: 15px;
        }

        /* Dataframe and chart styling */
        .stDataFrame, .stPlotlyChart {
            background-color: #ffffff;
            padding: 5px;
            border-radius: 10px;
        }

        /* Custom column styling */
        .stColumns {
            margin-top: 10px;
        }

        /* Styling for headers */
        h3 {
            font-size: 1.5em;
            color: #293241;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("📊 WhatsApp Chat Analyser")
st.sidebar.subheader("Upload and analyze your chat data")

# File upload and preprocessing
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.read()
    data = bytes_data.decode("utf-8")
    df = preprocess(data)

    # Fetch unique users for analysis
    user_list = df['users'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification') 
    user_list.sort()
    user_list.insert(0, "Overall")
    
    selected_user = st.sidebar.selectbox("Show analysis for", user_list)
    
    # Show Analysis button
    if st.sidebar.button("Show Analysis"):
        st.title("WhatsApp Chat Analysis")
        
        # ------------------ Statistics Section ------------------
        st.subheader("📈 Top Statistics")
        num_messages, words, num_media, url = fetch_stats(selected_user, df)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Messages", num_messages)
        col2.metric("Words", words)
        col3.metric("Media", num_media)
        col4.metric("Links", url)
        
        # ----------------- Monthly Timeline -----------------
        st.subheader("📅 Monthly Timeline")
        timeline = monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'], color='#457b9d')
        ax.set_title("Messages Over Time")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # ----------------- Daily Timeline -----------------
        st.subheader("📆 Daily Timeline")
        daily_timeline_data = daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline_data['only_date'], daily_timeline_data['messages'], color='#1d3557')
        ax.set_title("Messages by Day")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # ----------------- Activity Map -----------------
        st.subheader("📊 Activity Map")
        
        # Weekly Activity
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Weekly Activity**")
            week_activity = week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(week_activity.index, week_activity.values, color='#e63946')
            ax.set_title("Messages by Day of Week")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Monthly Activity
        with col2:
            st.write("**Monthly Activity**")
            month_activity = month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(month_activity.index, month_activity.values, color='#a8dadc')
            ax.set_title("Messages by Month")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # ----------------- Heatmap -----------------
        st.subheader("📅 Activity Heatmap")
        activity_heatmap_data = activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.heatmap(activity_heatmap_data, ax=ax, cmap='coolwarm')
        st.pyplot(fig)
        
        # ----------------- Busiest Users -----------------
        if selected_user == 'Overall':
            st.subheader("🧑‍🤝‍🧑 Busiest Users")
            x, dff = busiest_users(df)
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x, color='#e76f51')
                ax.set_title("Top Active Users")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.write("**User Statistics**")
                st.dataframe(dff)
        
        # ----------------- Word Cloud -----------------
        st.subheader("☁️ Word Cloud")
        df_wc = create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)

        # ----------------- Most Used Words -----------------
        st.subheader("📜 Most Used Words")
        most_common_words = most_used_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_words[0], most_common_words[1], color='#2a9d8f')
        ax.set_title("Most Frequent Words")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # ----------------- Most Used Emojis -----------------
        st.subheader("😊 Most Used Emojis")
        most_common_emojis = most_used_emojis(selected_user, df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(most_common_emojis)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(most_common_emojis[1].head(), labels=most_common_emojis[0].head(), autopct="%0.2f", colors=sns.color_palette("pastel"))
            st.pyplot(fig)
