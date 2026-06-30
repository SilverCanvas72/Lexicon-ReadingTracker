from re import search

import streamlit as st
import pandas as pd
from classes import Book

# Function: Load CSS - Takes CSS file_path parameter
#Keeping the CSS in ints own file helps the main python code to be more readable and removes the need for <style> tags at every element
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

#Load CSS
load_css("style.css")

pages = [
    st.Page('app_pages/home.py', title='Home', icon='🏠'),
    st.Page('app_pages/library.py', title='Library', icon='📖'),
    st.Page('app_pages/search.py', title='Search', icon='🔎'),
    st.Page('app_pages/stats.py', title='Statistics', icon='📊')
]
#note for later good video on navigation: https://www.youtube.com/watch?v=591rRCSEHt4

#Add pages to sidebar
pg = st.navigation(pages, position='sidebar', expanded=False)

#Run app
pg.run()


