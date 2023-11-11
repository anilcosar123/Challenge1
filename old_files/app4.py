import streamlit as st
import pandas as pd
 
st.write("""
# My first app
Hello *world!*
""")
 
df = pd.read_csv("C:/Users/anilp/Project_Files/EDA.csv")
st.line_chart(df)
df.head()