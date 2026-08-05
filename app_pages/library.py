import streamlit as st
from storage import save, load
from st_clickable_images import clickable_images
from app_pages.home import showBookPopup

def getFilteredBooks(unfilteredBooks, status, format, ownership):
    filteredBooks =[]
    if status != 'Any':
        for book in unfilteredBooks:
            if book.status == status:
                filteredBooks.append(book)
        return filteredBooks
    else:
        return(unfilteredBooks)


st.title('Library')

books = load()

# Set filters as allowing anything when the page first load and no filters have been set.
if "status" not in st.session_state:
    st.session_state.status = 'Any'
if "format" not in st.session_state:
    st.session_state.format = []
if 'ownership' not in st.session_state:
    st.session_state.ownership = []

st.set_page_config(layout="wide")


filteredBooks = getFilteredBooks(books, st.session_state.status, st.session_state.format, st.session_state.ownership)

imagePaths = []
for bookIndex in range (0, len(filteredBooks)):
    imagePaths.append(filteredBooks[bookIndex].getCover())

filteredBooksCol, filters = st.columns([3, 1])

with filteredBooksCol:
    clickedIndex = clickable_images(
            paths= imagePaths,
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "width": "100px", "height":"150px", "border-radius": "10px"},
    )
    if clickedIndex > -1:
            st.session_state.selectedBook = books[clickedIndex] #save book object temporarily to display correct popup
            st.session_state.selectedBookIndex = clickedIndex #TODO fix this system so the right popup shows
            showBookPopup()

with filters:
    with st.form("filterForm"):
        status = st.radio(
            label = "Status",
            options =["Any", "Read", "Reading", "Want To Read", "Did Not Finish"],

        )
        st.write("")

        st.write("Format")
        physical = st.checkbox("Physical")
        eBook = st.checkbox("eBook")
        audiobook = st.checkbox("Audiobook")

        st.write("")

        st.write("Ownership")
        owned = st.checkbox("Owned")
        borrowed = st.checkbox("Borrowed")
        wantToOwn = st.checkbox("Want to Own")
        wantToBorrow = st.checkbox("Want to Borrow")

        if st.form_submit_button("Filter"):
            st.session_state.status = status
            st.rerun()



#tagOptions = ['Owned', 'Borrowed', 'Want to Own', 'Want to Borrow', 'eBook', 'AudioBook', 'Print']


st.divider()

