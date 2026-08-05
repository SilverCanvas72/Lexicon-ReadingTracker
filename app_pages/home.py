import streamlit as st
from testData import tempBooks
from classes import Book
from storage import save, load

from st_clickable_images import clickable_images


# TODO - Fix page counts when changing books status

books = load()


@st.dialog('Edit')
#Pop Up displayed when reader want to add a session of reading
#They open the popup by pressing the 'add progress' button
#Readers can here enter their current page or percentage and how long they read for
#When they save their total pages read is calculated and tied to the time taken in the data for reading time estimations
def showBookPopup():
    st.empty()

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
            st.session_state.newPageInput = books[index].pageTotal
            st.number_input('', key='newPageInput', min_value=1, max_value = 3000, width=150, label_visibility="collapsed", on_change=saveBookPopup, args=(index,))


        pagesLeft = books[index].pageTotal - books[index].currentProgress
        st.write(f"Estimated Time To Finish: {minsToHours(calculateMinsPerPage(pagesLeft))} Hours")

    statusTagOptions = ['Read', 'Want To Read', 'Reading', 'Did Not Finish']

    st.session_state.newStatusInput = books[index].status
    st.pills("", statusTagOptions, selection_mode='single', on_change=saveBookPopup, args=(index,), key='newStatusInput')


    tagOptions = ['Owned', 'Borrowed', 'Want to Own', 'Want to Borrow', 'eBook', 'Audiobook', 'Physical']
    st.session_state.newTagInput = books[index].tags
    st.multiselect('', tagOptions, placeholder='Book Tags', label_visibility='collapsed', on_change=saveBookPopup, key='newTagInput', args=(index,))

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
                oldProgress = books[index].currentProgress #Temp variable for the last saved page number
                newProgress = st.number_input('', min_value=oldProgress, max_value=(books[index].pageTotal), width=150, label_visibility="collapsed", value=book.currentProgress, key='newProgressInput')
                pageDifference = newProgress - oldProgress #Find the amount of pages read before overwritting the old page number with the new one on the books list
                                                           #This is then used for the time estimate by adding the pages read and the amount of time it took to the list of dictionaries
            with total:
                newPageTotal = st.number_input('', min_value=books[index].currentProgress, max_value=3000, width=150, label_visibility="collapsed", value=book.pageTotal)

        #TODO: Create the logic for this, TRUE/FALSE vs PAGES/PERCENTAGES
        with pageBoolean:
                book.trackingPages = st.radio('', ['Pages', 'Percentages'], label_visibility="collapsed")

        timeInput, finishedButton, saveButton = st.columns([2,1,1])
        with timeInput:
            minsRead = st.number_input('Time in Session (mins)', value=None, min_value=0, max_value=180,)
        with finishedButton:
            st.write("") #Space fillers to place button inline with minutes input.

            st.write("")
            if st.button("Finish"):
                books[index].status = 'Read'
                save(books)
                st.rerun()  # To remove book from 'currently reading' part of homepage
        with saveButton:
            st.write("")
            st.write("")
            if st.button("Save"):
                books[index].totalMinsRead += minsRead
                books[index].readingSessions.append({'pagesRead': pageDifference, 'minsRead': minsRead})
                books[index].currentProgress = newProgress
                books[index].pageTotal = newPageTotal
                save(books)

                if newProgress >= books[index].currentProgress and newProgress <= books[index].pageTotal: #Makes sure popup only closes if inputed value is greater than or equal to the last current page input.
                                                                #The validation means a message will display when an incorrect message but this if statement prevents the windows form closing without the user seeing this message.
                    st.rerun() # Refreshes the page to update progress bars and book displays as well as collapsing popup
                               # This also keeps the page scrolled to the right place.
                            # TODO fix this so the pop-up does not close
                            # TODO Make input required for time read (Make a form with multiple submit buttons)


def saveBookPopup(index):
    books[index].status = st.session_state.newStatusInput
    books[index].tags = st.session_state.newTagInput
    books[index].pageTotal = st.session_state.newPageInput
    save(books)

def calculateMinsPerPage(pages):
    #Using each reading session an average minutes per page is created across all sorts of books of different page sizes
    #The function passes in the total pages to read and it returns the amount of time in minutes to read it.
    totalMins = 0
    totalPages = 0
    for book in books:
        for session in book.readingSessions:
            totalMins += session.get('minsRead')
            totalPages += session.get('pagesRead')
    if totalPages != 0:      #Make sure you are not dividing by zero to avoid error.
        minsPerPage = totalMins/totalPages
        return pages * minsPerPage
    else:
        return('Please add a reading session to calculate reading time averages')

def minsToHours(minutes):
    hours = round(minutes/60, 2)
    return(hours)


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

for bookIndex in range (0, (len(books))):
    if books[bookIndex].status == 'Reading':
        col1, col2 = st.columns([1, 3]) #Creates two columns, column 2 is 3 times as big as column 1

        with col1:

            st.image(books[bookIndex].getCover(), width=100)

        with col2:
            st.write(books[bookIndex].title)
            st.write(f"Time Read: {minsToHours(books[bookIndex].totalMinsRead)} hours")
            pagesLeft = books[bookIndex].pageTotal - books[bookIndex].currentProgress

            st.write(f"Time Left: {minsToHours(calculateMinsPerPage(pagesLeft))} Hours") #TODO: Write estimate time to read function and implement here
            progressCol, finishCol = st.columns([1, 2])

            with progressCol:
                if st.button('Add Progress', key=f'progress{books[bookIndex].title}'):
                    st.session_state.selectedBook = books[bookIndex]
                    st.session_state.selectedBookIndex = bookIndex
                    showProgressPopup()

            with finishCol:
                if st.button('✓', f'finish{books[bookIndex].isbn}'):
                    books[bookIndex].currentProgress = books[bookIndex].pageTotal
                    books[bookIndex].status = 'Read'
                    save(books)
                    st.rerun() # To remove book from 'currently reading' part of homepage

        st.progress((books[bookIndex].currentProgress/books[bookIndex].pageTotal))
        st.divider()


st.write('PopUp Tests')
st.divider()


imagePaths = []
for bookIndex in range (0, len(books)):
    imagePaths.append(books[bookIndex].getCover())

clickedIndex = clickable_images(
        paths= imagePaths,
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "width": "100px", "height":"150px", "border-radius": "10px"},
)
if clickedIndex > -1:
        st.session_state.selectedBook = books[clickedIndex] #save book object temporarily to display correct popup
        st.session_state.selectedBookIndex = clickedIndex
        showBookPopup()


st.divider()

