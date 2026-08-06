import json

#Classes:

#Book Class
#Every book is created as an object of this class, including temporary ones for search results

class Book:
    def __init__ (self, title, author, pubYear, pageTotal, genre, status, isbn):
        self.title = title
        self.author = author
        self.pubYear = pubYear
        self.pageTotal = pageTotal
        self.genres = genre #first genre associated with book
        self.tags = [] #list of tags the book has been tagged with
        self.isbn = isbn #reference used to display the books cover
        self.status = status # Current books stats options being : 'reading', 'read', 'wantToRead' and 'didNotFinish'
        self.readingSessions = [] # List of readingSession objects
        self.currentProgress = 0 #Current progress in pages, if tracking Pages is false, percentage can be calculated with this and total pages
        self.totalMinsRead = 0

    #For saving the book objects to the user's JSON file each object must be passed in as a dictionary
    def toDict(self):
        return {"title": self.title, "author": self.author, "pubYear": self.pubYear, "pageTotal": self.pageTotal, "genres": self.genres, "tags": self.tags, "isbn": self.isbn, "status": self.status ,"readingSessions": self.readingSessions, "currentProgress": self.currentProgress, "totalMinsRead": self.totalMinsRead}

    def getCover(self):
        if self.isbn == '': #Display a placeholder, no cover image as I save the isbn as '' if there is no coverID
            return('https://iarc-publications-website.s3.eu-west-3.amazonaws.com/media/default/0001/02/thumb_1296_default_publication.jpeg')
        else:
            return f'https://covers.openlibrary.org/b/id/{self.isbn}-L.jpg'

    #For recovering book objects from the saved JSON file, turns passed in JSON data back into object
    @classmethod
    def fromDict(Book, data):
        #Create book object from the dictionary
        book = Book(title = data["title"], author = data["author"], pubYear=data["pubYear"], pageTotal=data["pageTotal"], genre = data["genres"], status = data["status"], isbn = data["isbn"])


        #account for the three default values that don't need to be passed in to create a book but may have been changed since
        book.tags = data.get("tags")
        book.readingSessions = data.get("readingSessions")
        book.currentProgress = data.get("currentProgress")
        book.totalMinsRead = data.get("totalMinsRead")

        return book




