import requests
import streamlit as st


# Define your API key here
API_KEY = 'fba8e286495646148f8bc67700283455'

def get_investment_news():
    # Define the endpoint URL
    url = "https://newsapi.org/v2/everything"
    
    # Specify the query and number of returns
    parameters = {
        'q': 'stocks',  # or 'investment', 'finance', 'market', etc.
        'pageSize': 10,  # number of articles to return
        'apiKey': API_KEY,
        'language': 'en',  # retrieve English news
        'sortBy': 'publishedAt',  # sort by the latest articles
    }
    
    # Make the request
    response = requests.get(url, params=parameters)
    articles = response.json()['articles']
    
    # Return the articles list
    return articles

def display_news():
    st.title('Latest Investment News')
    
    # Get news articles from the API
    news_items = get_investment_news()
    
    # Display each news item
    for item in news_items:
        st.subheader(item['title'])
        st.write('Published at: ' + item['publishedAt'])
        st.write(item['description'])
        st.write('[Read More](' + item['url'] + ')', unsafe_allow_html=True)
        st.image(item['urlToImage'])
        st.write('---')

# Streamlit interface
if __name__ == "__main__":
    st.set_page_config(page_title="Investment News", page_icon=":newspaper:", layout='wide')
    display_news()

    