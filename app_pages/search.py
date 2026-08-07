import streamlit as st
import requests
from classes import Book
from storage import save, load

#SEARCH
# This page is where the user adds books from
# The open libraries API is used to source books from as it provides all needed information, all without the need for an api key
# The search is inputted by the user and the top 5 results (or less if less entries are returned) are displayed.
# The user can then add one of the books to their library by inputting how many pages it has, this will direct them to the library page displaying all books.


books = load()


# Parameter: response - the raw response from the API given the search query
# The function validates that a response was given, converts to json, saves the relevant data in books objects and returns a temporary list of these objects

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



#Parameters: searchResults - a list of book objects made from the APIs returns
# This function displays the temporary results objects and allows the user to add these books to their libraries
def displayResults(searchResults):

    if searchResults is None: #VALIDATION: Existence check
        st.write('Error Searching')

    if len(searchResults) == 0: #Check if searchResults = [] as that is what it is set to when there are no search results
        st.write('No Books Found')

    st.write("") #spacing
    st.write(f"Displaying {len(searchResults)} Results") # Tell the user how many results (usually 5 unless there were less returned)

    for bookIndex in range(0, (len(searchResults))):
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.image(searchResults[bookIndex].getCover(), width=100)

        with col2:
            # Display book data
            st.write(f'**{searchResults[bookIndex].title}**' )
            st.write(searchResults[bookIndex].author)
            st.write(f'{searchResults[bookIndex].pubYear}')

        with col3:
            # Form that requires the user to input the amount of pages in the book before they add it to their library.
            # This can be changed later but it provides the user with a direct pathway to do this instead of them trying to change the books total pages from the progress popup.
            with st.form( key=f'addBook{bookIndex}'):
                pages = st.number_input(min_value=1, max_value=3000, label='Pages', key=f'addPages{bookIndex}')
                submitted = st.form_submit_button("Add to Library")

                if submitted:
                    if pages==0 or pages==1:
                        st.error("The 'Pages' field is required. Please enter A value more than 2 and less than 3000")
                    else:
                        searchResults[bookIndex].pageTotal = pages
                        books.append(searchResults[bookIndex])

                        # Set the filters for the library page before directing there so that all books are displayed, not the filers from the last session
                        st.session_state.status = "Any"
                        st.session_state.filters = []
                        save(books)
                        st.switch_page('app_pages/library.py')
        st.divider()


if "searchResults" not in st.session_state:
    st.session_state.searchResults = ''

st.title('Search')


url = 'https://openlibrary.org/search.json' #Base url for query


# Search Bar, query is entered into the bar and passed directly to the api which fetches the top 5 results and returns into the search results.
with st.form("searchBar"):
    searchBar, searchBtn = st.columns([7 , 1])
    with searchBar:
        search = st.text_input("", max_chars=200, label_visibility="collapsed") #VALIDATION: range - max 200

    with searchBtn:
        if st.form_submit_button("Search") and search.strip(): #Checks that the search bar has a search term before searching
            params = {
                "q": search,
                "limit": 5
            }
            response = requests.get(url, params=params, verify=False)
            st.session_state.searchResults = getSearchResults(response)

displayResults(st.session_state.searchResults)

