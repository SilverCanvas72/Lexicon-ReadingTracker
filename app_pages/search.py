import streamlit as st
import requests
from classes import Book
from storage import save, load


def getSearchResults(response):
    if response.status_code != 200: #If the query was a failure:
        return None

    searchData = response.json()

    if searchData.get("numFound") == 0: #Check if there are any results, if not let the user know
        return []

    searchResults =[] #List of temporary book objects that only get appended to the books list if saved

    for book in searchData.get("docs", []):
        # Validation :
        # Make sure all books have appropriate values and if not set to a default to avoid errors and program crashes
        try:
            title = book['title']
        except KeyError:
            title = 'Title Not Found'

        try:
            author = book['author_name'][0]
        except KeyError:
            author = 'Author Not Found'

        try:
            pubYear = book['first_publish_year']
        except KeyError:
            pubYear = 'Year Published Not Found'

        try:
            isbn = book['cover_i']
        except KeyError:
            isbn = ''

        searchResults.append(Book(title, author, pubYear, 1, 'No Genre', 'Want To Read', isbn))
    return(searchResults)

def displayResults(searchResults):


    if searchResults is None:
        st.write('Error Searching')

    if len(searchResults) == 0: #Check if searchResults = [] as that is what it is set to when there are no search results
        st.write('No Books Found')

    for bookIndex in range(0, (len(searchResults))):
        col1, col2, col3 = st.columns([1, 2, 3])
        with col1:
            st.image(searchResults[bookIndex].getCover(), width=100)

        with col2:
            st.write(searchResults[bookIndex].title)
            st.write(searchResults[bookIndex].author)
            st.write(searchResults[bookIndex].genres)

        with col3:
            with st.form( key=f'addBook{bookIndex}'):
                pages = st.number_input(min_value=1, max_value=3000, label='Pages', key=f'addPages{bookIndex}')

                submitted = st.form_submit_button("Add to Library")

                if submitted:
                    if pages==0 or pages==1:
                        st.error("The 'Pages' field is required. Please enter A value more than 2 and less than 3000")
                    else:
                        searchResults[bookIndex].pageTotal = pages
                        books.append(searchResults[bookIndex])
                        st.session_state.status = "Any"
                        st.session_state.filters = []
                        save(books)
                        st.switch_page('app_pages/library.py')
        st.divider()



if "searchResults" not in st.session_state:
    st.session_state.searchResults = ''

books=load()

st.title('Search')

url = 'https://openlibrary.org/search.json'

with st.form("searchBar"):
    search = st.text_input("Search:", max_chars=200)

    if st.form_submit_button("Search") and search.strip(): #Checks that the search bar has a search term before searching
        params = {
            "q": search,
            "limit": 5
        }
        response = requests.get(url, params=params, verify=False)
        st.session_state.searchResults = getSearchResults(response)

displayResults(st.session_state.searchResults)

