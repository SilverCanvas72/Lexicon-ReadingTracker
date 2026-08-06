import streamlit as st
from storage import save, load
from st_clickable_images import clickable_images
from app_pages.home import showBookPopup


# TODO - Fix filter defaults, refresh when page is reopened
def getFilters():
    filters = []
    if physical:
        filters.append("Physical")
    if eBook:
        filters.append("eBook")
    if audiobook:
        filters.append("Audiobook")
    if owned:
        filters.append("Owned")
    if borrowed:
        filters.append("Borrowed")
    if wantToOwn:
        filters.append("Want to Own")
    if wantToBorrow:
        filters.append("Want to Borrow")

    return(filters)

def getFilteredBooks(status, filters):

    filteredBooksIndex =[]
    if status != 'Any':
        for bookIndex in range (0, len(books)):
            if books[bookIndex].status == status:
                filteredBooksIndex.append(bookIndex)
    else:
        for bookIndex in range (0, len(books)):
            filteredBooksIndex.append(bookIndex)

    tempIndex = 0
    for bookIndex in filteredBooksIndex:
        for filter in filters:
            if filter not in books[bookIndex].tags:
                filteredBooksIndex[tempIndex] = -1
        tempIndex += 1

    filteredBooksIndex = [item for item in filteredBooksIndex if item != -1]
    return filteredBooksIndex



st.title('Library')

books = load()

# Set filters as allowing anything when the page first load and no filters have been set.
if "status" not in st.session_state:
    st.session_state.status = 'Any'
if "filters" not in st.session_state:
    st.session_state.filters = []

st.set_page_config(layout="wide")


filteredBooks = getFilteredBooks(st.session_state.status, st.session_state.filters)

imagePaths = []
for bookIndex in filteredBooks:
    imagePaths.append(books[bookIndex].getCover())

filteredBooksCol, filters = st.columns([3, 1])

with filteredBooksCol:

    if filteredBooks == []:
        st.write('No Books Found')
    else:
        st.toast("Loading...", icon='⏳',duration=2)
    clickedIndex = clickable_images(
            paths= imagePaths,
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "width": "100px", "height":"150px", "border-radius": "10px"},
    )
    if clickedIndex > -1:
            st.session_state.selectedBook = books[filteredBooks[clickedIndex]] #save book object temporarily to display correct popup
            st.session_state.selectedBookIndex =filteredBooks[clickedIndex]
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
            st.session_state.filters = getFilters()
            st.write(getFilteredBooks(st.session_state.status, st.session_state.filters))
            st.rerun()



#tagOptions = ['Owned', 'Borrowed', 'Want to Own', 'Want to Borrow', 'eBook', 'AudioBook', 'Print']


st.divider()

