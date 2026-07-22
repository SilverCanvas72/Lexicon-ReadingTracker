import json

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

    #For saving the book objects to the user's JSON file each object must be passed in as a dictionary
    def toDict(self):
        return {"title": self.title, "author": self.author, "pubYear": self.pubYear, "pageTotal": self.pageTotal, "genres": self.genres, "tags": self.tags, "trackingPages": self.trackingPages, "isbn": self.isbn, "readingSessions": self.readingSessions, "currentProgress": self.currentProgress, "totalMinsRead": self.totalMinsRead}

    def updateProgress(self):
        pass

    def getCover(self):
        return f"https://covers.openlibrary.org/b/isbn/{self.isbn}-L.jpg"

    #For recovering book objects from the saved JSON file, turns passed in JSON data back into object
    @classmethod
    def fromDict(Book, data):
        #Create book object from the dictionary
        book = Book(
            title = data["title"], author = data["author"], pubYear=data["pubYear"], pageTotal=data["pageTotal"], genre = data["genres"], tags = data["tags"], trackingPages = data["trackingPages"], isbn = data["isbn"]
        )

        #account for the three default values that dont need to be passed in to create a book but may have been changed since
        book.readingSessions = data.get("readingSessions")
        book.currentProgress = data.get("currentProgress")
        book.totalMinsRead = data.get("totalMinsRead")

        return book




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

