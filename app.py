import streamlit as st

#----------------------
#LEXICON
# Program Name: Lexicon - Reading Tracker
# Version 1.0
# Naming Convention : camelCase for all variable and function names, Class names are in Pascal Case
#Description / Overview:
    # This project uses Streamlit to form its web interface from the python scripts as well as including a .css file
    #         for technical styling not within the range of Streamlit's functionality.
    # + The streamlit book tracker allows users to:
    #     + Add books from the Open Libraries API
    #     + Add progress on their books including pages read and time taken
    #     + This data is used to estimate how long it will take users to finish books or read unstarted books
    #     + Users can search their 'library' (all their added books) by tags that they set for each book including:
    #         + Read, Reading, Want to Read and Did not Finish
    #         + Ebook, Audiobook and Print
    #         + Want to Own, Want to Borrow, Borrowed and Owned
    #     + All books data is stored in a JSON file local to the user so they can refresh or close the page and come back later
    # Full Feature lists as well as functional and non-functional requirements can be read in the SRS document

st.set_page_config(layout="centered") #sets default for pages to have wide margins, this is changed on a case by case basis, namely for the library page

# Function: Load CSS - Takes CSS file_path parameter
#Keeping the CSS in ints own file helps the main python code to be more readable and removes the need for <style> tags at every element
def loadCss(filePath):
    with open(filePath) as f:
        st.html(f"<style>{f.read()}</style>")

#Load CSS
loadCss("style.css")


#Navigation and sidebar setup
pages = [
    st.Page('app_pages/home.py', title='Home', icon='🏠'),
    st.Page('app_pages/library.py', title='Library', icon='📖'),
    st.Page('app_pages/search.py', title='Search', icon='🔎'),
]

#Add pages to sidebar
pg = st.navigation(pages, position='sidebar', expanded=False)

#Run app
pg.run()