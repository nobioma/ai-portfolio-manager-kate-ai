import os
import streamlit as st
from openai import AzureOpenAI, Stream
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import requests
import json


# Load env variables
load_dotenv(find_dotenv())
os.environ["SSL_CERT_FILE"] = os.getenv("REQUESTS_CA_BUNDLE")
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

### Do not remove the above code ###

response = ""

def isolateTicker(response):
    tickers = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "system", "content": """Take the companies mentioned and return their ticker simples in a specific format. 
                       Nothing but the tickers should be returned in the output. The format should be in the form of their tickers separated
                        by commas surrounded by curly braces. Example: {AAPL, MSFT, AI}"""}, {"role": "user", "content":response}],
            stream = False
    ).choices[0].message.content

def getChartData(response):
    tickers = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "system", "content": """Find the stock symbols and their corresponding allocation percentages and return in a specific format.
            Example: if Apples allocation percentage is 25 and Microsoft's allocation percentage is 30 return this only ['AAPL', 'MSFT']+[25, 30] remember the addition sign separates the two lists"""}, {"role": "user", "content":response}],
            stream = False
    ).choices[0].message.content

    return tickers

def separate_lists(input_str):
    # Split the input string at '], [', removing leading and trailing brackets
    lists = input_str.strip('[]').split(']+[')

    # Extract list 1 and list 2
    list1_str = lists[0]
    list2_str = lists[1]
    
    return list1_str, list2_str

def getRisk(response):
    risk = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "system", "content": """Based on the response list different scenerios that can happen in the market and how the portfolio will perform. Show the exact profit and loss for each one. Also include what risks or limitations the portfolio has and how it can be improved. Organize this data in a concise way to e displayed on a web page"""}, {"role": "user", "content":response}],
            stream = False
    ).choices[0].message.content

    return risk

def getProfile(response):
    risk = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "system", "content": """Based on the user input display a profile of his/her characteristics. Example name, age, investing experience level, experience, interests, risk appetite(High, Medium, Low) and amount of cash to be invested. Display this information on different lines and make it look Bold """}, {"role": "user", "content":response}],
            stream = False
    ).choices[0].message.content

    return risk

#########FactSetAPI#########
############################

st.set_page_config(
    page_title="ChatGPT Clone", 
    page_icon=":robot:", 
    layout='wide', 
    initial_sidebar_state='expanded'
)

col1, col2 = st.columns(2, gap = 'large')
col1.title("I'm Kate.Ai, your Artificial Portfolio Manager!")


    #st.selectbox("Model Version", ("gpt-4", "gpt-3.5"))
    #st.slider("Response Length", min_value=50, max_value=500, value=150)


col1.write(" Please enter your name, age, investing experience level, investment interests (sectors, asset classes, ect.), risk appetite(low, moderate, or high), and amount of cash to be invested.")


client = AzureOpenAI(
    api_version="2024-02-01",
    azure_endpoint=os.getenv("OPENAI_API_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

if "openai_client" not in st.session_state:
    st.session_state["openai_client"] = client


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type Here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "system", "content": """Hello! My name is Kate, your Artificial Portfolio Manager. To tailor my recommendations for your investment portfolio, I need some information from you. Could you kindly share your 
                       current job or industry, your age, risk tolerance(High, medium, low) and how familiar you are with investment terms (beginner, intermediate, advanced)? Additionally, please let me know your investment goals such as seeking long-term growth, short term profits, or a mix of both. I'm also curious about 
                       which types of companies or sectors you are interested in. Based on the details you provide, I will generate a personalized list of stock recommendations (More of a command like give a concrete list of what stocks to include) from companies 
                       that align with your interests, categorized to reflect your preferences. Also, provide how much money you have available to invest so I can return a the specific allocation of cash for the stocks. If your knowledge of investment terms is limited, I will ensure all explanations are easy to understand. I'll also offer 
                       general investing advice and tips suited to your knowledge level and goals. Furthermore, I will periodically review and update your portfolio to adapt to any changes in your objectives or the market conditions. 
                       If you have any questions or need further clarification on any topic, feel free to ask at any time. 
                       Let's embark on your investment journey together! Make sure the portfolio has 30 holding and is diversified among asset classes if applicable"""}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
    chartData = (getChartData(response))
    st.session_state['risk'] = getRisk(response)
    st.session_state['profile'] = getProfile(prompt)



#########################################################






 #####################################################   



#st.caption("Navigate to the output page from the sidebar to see the investment graph based on your preferences.")



 ###########################################################

#API SECTION DO NOT CHANGE

url = 'https://api.factset.com/report/overview/v1/profile?id=FDS'
api_key = '...'

# Set up the headers dictionary to include the API key
headers = {
    'Authorization': f'Bearer {api_key}'
}

# Make the GET request
response = requests.get(url, headers=headers)

print(response.json)

#####################################################################