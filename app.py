import streamlit as st
import pandas as pd

# Function: Load CSS - Takes CSS file_path parameter
#Keeping the CSS in ints own file helps the main python code to be more readable and removes the need for <style> tags at every element
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

#Load CSS
load_css("style.css")

#Page elements:
st.markdown("""
    <div class='logo'>Lexicon</div>
    """, unsafe_allow_html=True)
st.divider()
st.markdown("""
    <div class='sub-heading'>Currently Reading</div>
    """,unsafe_allow_html=True
)
st.divider()




