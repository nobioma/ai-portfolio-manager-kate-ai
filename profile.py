



import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import altair as alt
import pandas as pd



st.title('User Profile')

while 'profile' not in st.session_state:
    pass

st.write(st.session_state['profile'])

