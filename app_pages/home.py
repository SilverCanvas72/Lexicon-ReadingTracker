#Imports: streamlit, Book class, save and load functions for JSON handling

import streamlit as st
from classes import Book
from storage import save, load

# HOMEPAGE
# Here the books the user are currently reading are displayed and they can add their progress for each.
# File also contains functions for the display of pop-ups within the app (Progress and Book)

books = load()  #LIST: Immediately import the list of books from the JSON file to make sure the most up-to-date one is used

@st.dialog('Edit')
# This popup comes from when a user clicks the books cover from the library page.
# This is where the user can change the books, tags, status and page count as well as seeing data on how long it will take to read.
# Each input is validated and saved after input, a save button is not used.
# there are no parameters to the function, the clicked books index is pulled from the session state.

def showBookPopup():
    st.empty() # Remove any data the popup's temp variables may have retained from other times they were opened
    books = load()

    # These values are saved to session state right before the showBookPopup function is called
    book = st.session_state.selectedBook #load in the book object from the users temporary local storage
    index = st.session_state.selectedBookIndex # load in the index of the selected book from the user's temp local storage

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
            st.session_state.newPageInput = books[index].pageTotal #save the current pageTotal to a session state for the default value of input
            st.number_input('', key='newPageInput', min_value=1, max_value = 3000, width=150, label_visibility="collapsed", on_change=saveBookPopup, args=(index,))  # func saveBookPopup is called after the data has been validated to save data

        pagesLeft = books[index].pageTotal - books[index].currentProgress
        if (calculateMinsPerPage(pagesLeft)) != 0: #VALIDATION Make sure there is reading sessions to calculate the reading estimate. Make sure no dividing by zero errors
            st.write(f"Time Left: {minsToHours(calculateMinsPerPage(pagesLeft))} Hours")
        else:
            st.write('Please log a reading session to get reading estimates') #Message if user has no reading sessions




    statusTagOptions = ['Read', 'Want To Read', 'Reading', 'Did Not Finish']

    # Save current status and load into status select.
    st.session_state.newStatusInput = books[index].status
    st.pills("", statusTagOptions, selection_mode='single', on_change=saveBookPopup, args=(index,), key='newStatusInput')

    tagOptions = ['Owned', 'Borrowed', 'Want to Own', 'Want to Borrow', 'eBook', 'Audiobook', 'Physical']
    # Save current tags and load into tag select
    st.session_state.newTagInput = books[index].tags
    st.multiselect('', tagOptions, placeholder='Book Tags', label_visibility='collapsed', on_change=saveBookPopup, key='newTagInput', args=(index,))




@st.dialog('Progress Edit')
#Pop Up displayed when reader want to add a session of reading
#They open the popup by pressing the 'add progress' button on the homepage
#Readers can here enter their current page and how long they read for
#When they save their total pages read is calculated and tied to the time taken in the data for reading time estimations
# No parameters are needed, the book to display is saved in local storage
def showProgressPopup():

    # Load book and index from session state
    book = st.session_state.selectedBook
    index = st.session_state.selectedBookIndex


    cover, info = st.columns([2, 5])
    with cover:
        st.image(book.getCover(), width=100)
    with info:
        # Write basic data
        st.write(book.title)
        st.progress((book.currentProgress / book.pageTotal))


        with st.form("progressForm"): #Creation of form, this means no data is saved until after the save button is clicked and all data is validated

            input,total = st.columns([1,1])
            with input:

                oldProgress = books[index].currentProgress #Temp variable for the last saved page number
                newProgress = st.number_input('Current Page', min_value=oldProgress, max_value=(books[index].pageTotal), width=150, value=book.currentProgress, key='newProgressInput')
                pageDifference = newProgress - oldProgress #Find the amount of pages read before overwritting the old page number with the new one on the books list
                                                           #This is then used for the time estimate by adding the pages read and the amount of time it took to the list of dictionaries
            with total:
                newPageTotal = st.number_input('Page Total', min_value=books[index].currentProgress, max_value=3000, width=150, value=book.pageTotal)

            timeInput, saveButton = st.columns([2,1])
            with timeInput:
                minsRead = st.number_input('Time in Session (mins)', value=None, min_value=0, max_value=180,)

            with saveButton:

                st.write("") #Button positioning to make it inline with the time input, not the time label
                st.write("")

                submitted = st.form_submit_button("Save") # create ave button
                if submitted:
                    # VALIDATION
                    if oldProgress == newProgress: # If no pages are read, the user does not change the current page input
                        st.error("Please input a new current page higher than the old value.") #Write error popup

                    elif minsRead == None: # If no input for the time read
                        st.error("Please Input a valid time") #Write error popup

                    elif newProgress == newPageTotal: # If both are equal the book must be finished
                        books[index].status = 'Read'
                        save(books)
                        st.rerun()

                    elif newPageTotal < newProgress: #Check the user hasn't read more pages than in the book.
                        st.error("Total pages must be greater than or equal to current page")

                    else:
                        # Save all inputs if passes all validation tests.
                        books[index].totalMinsRead += minsRead
                        books[index].readingSessions.append({'pagesRead': pageDifference, 'minsRead': minsRead})
                        books[index].currentProgress = newProgress
                        books[index].pageTotal = newPageTotal
                        save(books)
                        st.rerun()


# Called after making an input to the book popup as there is no save button
# All data passed into this will be valid, the inputs have minimums, maximums and status has multiselect off
def saveBookPopup(index):
    books = load()
    books[index].status = st.session_state.newStatusInput
    books[index].tags = st.session_state.newTagInput
    books[index].pageTotal = st.session_state.newPageInput
    save(books)


# Parameters : Pages - The amount of pages to be read
# The function calculates how long it will take to rad the inputted amount of pages based on past reading session times.
# The function uses all session logs from all books to create a more accurate average for a range of font or page sizes.

def calculateMinsPerPage(pages):
    #Using each reading session an average minutes per page is created across all sorts of books of different page sizes
    #The function passes in the total pages to read and it returns the amount of time in minutes to read it.
    totalMins = 0
    totalPages = 0
    for book in books:
        for session in book.readingSessions: # For every book in the users library look at every reading session associated.
            totalMins += session.get('minsRead')
            totalPages += session.get('pagesRead')
    if totalPages != 0:      #Make sure you are not dividing by zero to avoid error.
        minsPerPage = totalMins/totalPages # Create and average mins/page
        return pages * minsPerPage
    else:
        return(0)

#Paramter: minutes - the amount of minutes to convert to hours.
def minsToHours(minutes):
    hours = round(minutes/60, 2) # Only return up to 2 decimal points
    return(hours)


st.markdown("""
    <div class='logo'>Lexicon</div>
    """, unsafe_allow_html=True)
st.divider()
st.markdown("""
    <div class='subHeading'>Currently Reading</div>
    """,unsafe_allow_html=True
)
st.divider()

booksDisplayed = False # Boolean value that will be used to see if any books are shown, if this value is false a message will prompt the reader to add a book from the search page
for bookIndex in range (0, (len(books))):
    if books[bookIndex].status == 'Reading': # Only display books that are currently being read
        booksDisplayed = True # As soon as one book is found set this to try so the no books found message is not written
        col1, col2 = st.columns([1, 3]) #Creates two columns, column 2 is 3 times as big as column 1

        with col1:
            st.image(books[bookIndex].getCover(), width=100)

        with col2:
            # Write basic data
            st.write(books[bookIndex].title)
            st.write(f"Time Read: {minsToHours(books[bookIndex].totalMinsRead)} hours")
            pagesLeft = books[bookIndex].pageTotal - books[bookIndex].currentProgress

            #Calculate time to read
            if (calculateMinsPerPage(pagesLeft)) != 0:
                st.write(f"Time Left: {minsToHours(calculateMinsPerPage(pagesLeft))} Hours")
            else:
                st.write('Please log a reading session to get reading estimates')

            progressCol, finishCol = st.columns([1, 2])

            with progressCol:
                if st.button('Add Progress', key=f'progress{books[bookIndex].title}'):

                    st.session_state.selectedBook = books[bookIndex] #Save the book to the temp local storage
                    st.session_state.selectedBookIndex = bookIndex # save the books inde to the temp local storage
                    showProgressPopup() # display the book, this is done with the index and book just saved to the session state

            with finishCol:
                if st.button('✓', f'finish{books[bookIndex].isbn}'):
                    books[bookIndex].currentProgress = books[bookIndex].pageTotal
                    books[bookIndex].status = 'Read'
                    save(books)
                    st.rerun() # To remove book from 'currently reading' part of homepage

        st.progress((books[bookIndex].currentProgress/books[bookIndex].pageTotal)) # Progress bar, pass in the percentage read by dividing current and total pages
        st.divider()

#Display prompt if user is yet to add any books to currently reading
if booksDisplayed == False:
    st.write("You are currently not reading any books")
    st.write("Go to the Search page to add a book")
    st.write("Change a book's status from the library page")
