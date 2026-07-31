import streamlit as st
from storage import save, load
st.title('Library')

books = load()

for book in books:
    st.write(book)
    st.write(book.tags)
    for tag in book.tags:
        st.write(tag)
        if tag == 'reading':
            st.write(book)