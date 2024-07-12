import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
import pandas as pd

st.title('Risk and Scenarios')

while 'risk' not in st.session_state:
    pass

st.write(st.session_state['risk'])

