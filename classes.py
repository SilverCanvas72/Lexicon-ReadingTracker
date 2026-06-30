#Classes:
class Book:
    def __init__ (self, title, author, pubYear, pageTotal, genre, tags, trackingPages, isbn):
        self.title = title
        self.author = author
        self.pubYear = pubYear
        self.pageTotal = pageTotal
        self.genres = genre #first genre associated with book
        self.tags = tags #list of tags the book has been tagged with
        self.trackingPages = trackingPages #Boolean value determining if book is being tracked with pages or percentage
        self.isbn = isbn #reference used to display the books cover
        self.readingSessions = [] # List of readingSession objects
        self.currentProgress = 0 #Current progress in pages, if trackingPages is false, percentage can be calculated with this and total pages
        self.totalMinsRead = 0

    def updateProgress(self):
        pass

    def getCover(self):
        return f"https://covers.openlibrary.org/b/isbn/{self.isbn}-L.jpg"

class ReadingSession:
    def __init__(self, date, pagesRead, timeRead):
        self.date = date
        self.pagesRead = pagesRead
        self.timeRead = timeRead

class BookManager:
    def __init__(self):
        self.books = [] #List of all book objects
        self.goal = {} #Dictionary of user goal, filled in when users sets one

    #Function used to get an estimate for time a book will take to finish or read completely based on the amount of pages
    def calculateTimeToRead(self, pages):
        pass

    #Used for making graphs, type refers to the data wanted e.g. ownership or genres
    def getData (self, dateMin, dateMax, type):
        pass

    #Returns list of books to display
    def filterBooks(self, filters):
        # filter books = filteredBooks
        return filteredBooks

