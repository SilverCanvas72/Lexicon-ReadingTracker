import streamlit as st
from testData import tempBooks
from classes import Book
from storage import save, load

if st.button('test storage'):

    save(tempBooks)

    tempBooks[0].title = "test"
    save(tempBooks)

    books = load()
    st.write(books[0].title)

@st.dialog('Edit')
#Pop Up displayed when reader want to add a session of reading
#They open the popup by pressing the 'add progress' button
#Readers cna here enter their current page or percentage and how long they read for
#When they save their total pages read is calculated and tied to the time taken in the data for reading time estimations
def showBookPopup():
    book = st.session_state.selectedBook #temporarily stored selected book object when the add progress button is clicked.
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
            newPageTotal = st.number_input('', key=f'pages{book.title}', min_value=1, max_value = 3000, width=150, label_visibility="collapsed", value=book.pageTotal)
            book.pageTotal = newPageTotal
        st.write("Estimated Time: XX:XX Hours")
        book.pageTotal = st.session_state[f"pages{book.title}"]
    statusTagOptions = ['Read', 'Want To Read', 'Reading', 'Did Not Finish']
    book.tags = st.pills("", statusTagOptions, selection_mode='single')

    tagOptions = ['Owned', 'Borrowed', 'Want to Own', 'Want to Borrow', 'ebook', 'AudioBook', 'Print']
    tags = st.multiselect('', tagOptions, placeholder='Book Tags', label_visibility='collapsed')



@st.dialog('Progress Edit')
def showProgressPopup():
    book = st.session_state.selectedBook
    cover, info = st.columns([2, 5])

    with cover:
        st.image(book.getCover(), width=100)
    with info:
        st.write(book.title)
        st.progress((book.currentProgress / book.pageTotal) * 100)
        pageInput, pageBoolean = st.columns([3, 2])
        with pageInput:
            input,total = st.columns([1,1])
            with input:
                newProgress = st.number_input('', key=f'pageProgress{book.title}', min_value=0, max_value=3000, width=150, label_visibility="collapsed", value=book.currentProgress)
                book.newProgress = newProgress
            with total:
                st.number_input('', key=f'pages{book.title}', min_value=0, max_value=3000, width=150, label_visibility="collapsed", value=book.pageTotal)
        with pageBoolean:
                book.trackingPages = st.radio('', ['Pages', 'Percentages'], label_visibility="collapsed")
        timeInput, finishedButton, saveButton = st.columns([2,1,1])
        with timeInput:
            st.time_input('Time Read in Session')
        with finishedButton:
            st.button("Finish")
        with saveButton:
            st.button("Save")




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
            if st.button('Add Progress', key=f'progress{book.title}'):
                st.session_state.selectedBook = book
                showProgressPopup()

        with finishCol:
            st.button('✓', f'finish{book.isbn}')

    st.write(book.pageTotal)
    st.write(book.currentProgress)
    st.progress((book.currentProgress/book.pageTotal)*100)
    st.divider()

st.write('PopUp Tests')
st.divider()
for book in tempBooks:
    st.image(book.getCover(), width=50)

    if st.button("", key=(book.title)):
        st.session_state.selectedBook = book #save book key temporarily to display correct popup
        showBookPopup()
st.divider()

