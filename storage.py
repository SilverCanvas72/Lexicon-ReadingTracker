from classes import Book
import json


# saves current book objects and their attributes to the user's local JSON file
def save(unsaved):
    bookDictionaries = []
    for book in unsaved:
        bookDictionaries.append(book.toDict())

    with open("books.json", "w") as f:
        json.dump(bookDictionaries, f, indent=2)

# loads all past data from the user's local JSON file
def load():
    with open("books.json", "r") as f:
        loadedBooks = json.load(f)
        books = [Book.fromDict(item) for item in loadedBooks]
    return books