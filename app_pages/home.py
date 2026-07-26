import streamlit as st
from testData import tempBooks
from classes import Book
from storage import save, load

books = load()


@st.dialog('Edit')
#Pop Up displayed when reader want to add a session of reading
#They open the popup by pressing the 'add progress' button
#Readers cna here enter their current page or percentage and how long they read for
#When they save their total pages read is calculated and tied to the time taken in the data for reading time estimations
def showBookPopup():
    book = st.session_state.selectedBook #temporarily stored selected book object when the add progress button is clicked.
    index = st.session_state.selectedBookIndex
    cover, info = st.columns([2, 5])
    with cover:
        st.image(book.getCover(), width=200)
    with info:
        st.write(book.title)
        st.write(f'{book.author}  |  {book.pubYear}')
        label, pageInput = st.columns([1,2])
        with label:
            st.write('Pages:')
        with pageInput:
            books[index].pageTotal = st.number_input('', key=f'pages{book.title}', min_value=1, max_value = 3000, width=150, label_visibility="collapsed", value=book.pageTotal)
            save(books)
            #TODO Estimated tome logic.
        st.write("Estimated Time: XX:XX Hours")
        book.pageTotal = st.session_state[f"pages{book.title}"]
    statusTagOptions = ['Read', 'Want To Read', 'Reading', 'Did Not Finish']
    book.tags = st.pills("", statusTagOptions, selection_mode='single')

    tagOptions = ['Owned', 'Borrowed', 'Want to Own', 'Want to Borrow', 'ebook', 'AudioBook', 'Print']
    tags = st.multiselect('', tagOptions, placeholder='Book Tags', label_visibility='collapsed')



@st.dialog('Progress Edit')
def showProgressPopup():
    book = st.session_state.selectedBook
    index = st.session_state.selectedBookIndex
    cover, info = st.columns([2, 5])

    with cover:
        st.image(book.getCover(), width=100)
    with info:
        st.write(book.title)
        st.progress((book.currentProgress / book.pageTotal))
        pageInput, pageBoolean = st.columns([3, 2])
        with pageInput:
            input,total = st.columns([1,1])
            with input:
                newProgress = st.number_input('', key=f'pageProgress{book.title}', min_value=0, max_value=3000, width=150, label_visibility="collapsed", value=book.currentProgress)
                books[index].currentProgress = newProgress

            with total:
                newPageTotal = st.number_input('', key=f'pages{book.title}', min_value=0, max_value=3000, width=150, label_visibility="collapsed", value=book.pageTotal)
                books[index].pageTotal = newPageTotal

        #TODO: Create the logic for this, TRUE/FALSE vs PAGES/PERCENTAGES
        with pageBoolean:
                book.trackingPages = st.radio('', ['Pages', 'Percentages'], label_visibility="collapsed")

        timeInput, finishedButton, saveButton = st.columns([2,1,1])
        with timeInput:
            st.time_input('Time Read in Session', value=None) #TODO time input only allows increments of 15 mins
        with finishedButton:
            if st.button("Finish"):
                #TODO: Should there just be a singular reading status and then other tags to make this easier?
                pass
        with saveButton:
            if st.button("Save"):
                save(books)
                st.rerun() # Refreshes the page to update progress bars and book displays as well as collapsing popup
                           # This also keeps the page scrolled to the right place.



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

load()

for bookIndex in range (0, len(books)):
    col1, col2 = st.columns([1, 3]) #Creates two columns, column 2 is 3 times as big as column 1

    with col1:
        st.image(books[bookIndex].getCover(), width=100)

    with col2:
        st.write(books[bookIndex].title)
        st.write(f"Time Read: {round(books[bookIndex].totalMinsRead/60, 2)} hours")
        st.write("Time Left: XX.XX hours") #TODO: Write estimate time to read function and implement here
        progressCol, finishCol = st.columns([1, 2])

        with progressCol:
            if st.button('Add Progress', key=f'progress{books[bookIndex].title}'):
                st.session_state.selectedBook = books[bookIndex]
                st.session_state.selectedBookIndex = bookIndex
                showProgressPopup()

        with finishCol:
            st.button('✓', f'finish{books[bookIndex].isbn}')
    st.progress((books[bookIndex].currentProgress/books[bookIndex].pageTotal))
    st.divider()


st.write('PopUp Tests')
st.divider()

for bookIndex in range (0, len(books)):
    st.image(books[bookIndex].getCover(), width=50)

    if st.button("", key=books[bookIndex].title):
        st.session_state.selectedBook = books[bookIndex] #save book object temporarily to display correct popup
        st.session_state.selectedBookIndex = bookIndex
        showBookPopup()
st.divider()

