import streamlit as st
from testData import tempBooks
from classes import Book

st.title('Homepage')

st.markdown("""
    <div class='logo'>Lexicon</div>
    """, unsafe_allow_html=True)
st.divider()
st.markdown("""
    <div class='subHeading'>Currently Reading</div>
    """,unsafe_allow_html=True
)
st.divider()


for book in tempBooks:
    col1, col2 = st.columns([1, 3]) #Creates two columns, column 2 is 3 times as big as column 1

    with col1:
        st.image(book.getCover(), width=100)

    with col2:
        st.write(book.title)
        st.write(f"Time Read: {round(book.totalMinsRead/60, 2)} hours")
        st.write("Time Left: XX.XX hours") #TODO: Write estimate time to read function and implement here
        progressCol, finishCol = st.columns([1, 2])
        with progressCol:
            st.button('Add Progress', book.title) #This key is just a placeholder before I implement a better system for button id's as you cannot have dupplicates
        with finishCol:
            st.button('✓', book.isbn) #Placeholder button ID
    st.write('Make progress bar here')
    st.divider()