import streamlit as st
from storage import save, load
from st_clickable_images import clickable_images
from app_pages.home import showBookPopup

#LIBRARY
# This page displays all of the users saved books (library)
# The users can search books by applying filters on the right hand side of the page
# All of the filtered books are displayed with their covers, by clicking on the cover the bookPopup function is called and displayed.
# This page can be navigated to through the nav bar. It is also navigated to automatically when a book is added form the search page


def getFilters():
    filters = []
    # For each checkbox (filter) a boolean value is associated, if it is True it has been checked, and is added to the list of things to filter by
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


# Parameters:
#   + status : the status to filter by, if 'any' books of all status will be displayed
#   + filters: the list of tags (filters) to filter by.
#Returns:
#   + The function returns a list of the indexes of the filtered books. the indexes relate to their place in the BOOKS list, not the filtered books list.
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
                filteredBooksIndex[tempIndex] = -1 #Books that don't match the filter are marked -1 and removed below
        tempIndex += 1

    filteredBooksIndex = [item for item in filteredBooksIndex if item != -1] # here only indexes of books that match the filter (not -1) are kept.
    return filteredBooksIndex



st.title('Library')


# Set filters as allowing anything when the page first load and no filters have been set.
if "status" not in st.session_state:
    st.session_state.status = 'Any'
if "filters" not in st.session_state:
    st.session_state.filters = []


# As there is a column of filters and the books display the large margins used on the other pages cannot be used here so the layout has to be set to wide
st.set_page_config(layout="wide")

books = load()


filteredBooks = getFilteredBooks(st.session_state.status, st.session_state.filters)

imagePaths = []
for bookIndex in filteredBooks:
    imagePaths.append(books[bookIndex].getCover())

filteredBooksCol, filters = st.columns([3, 1])

with filteredBooksCol:

    if filteredBooks == []:
        st.write('No Books Found')
    else:
        st.toast("Loading...", icon='⏳',duration=2) #So it is clear to the user that the images are loading when there is books to load a temporary loading popup is displayed.
    clickedIndex = clickable_images(
            paths= imagePaths,
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "width": "100px", "height":"150px", "border-radius": "10px"},
    )
    if clickedIndex > -1:
            st.session_state.selectedBook = books[filteredBooks[clickedIndex]] #save book object temporarily to display correct popup
            st.session_state.selectedBookIndex =filteredBooks[clickedIndex] #save book index object temporarily to display correct popup
            showBookPopup()

with filters:

    with st.form("filterForm"):
        status = st.radio( #Radio buttons are used here as only one option can be chosen
            label = "Status",
            options =["Any", "Read", "Reading", "Want To Read", "Did Not Finish"],

        )
        st.write("")


        #Checkboxes that return boolean value for each make it easy to append the selected filters to a list which is looped through to filter books
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
            st.session_state.status = status #Save status to filter by to session state
            st.session_state.filters = getFilters() # Save filters to filter by
            st.write(getFilteredBooks(st.session_state.status, st.session_state.filters))
            st.rerun()


st.divider()

