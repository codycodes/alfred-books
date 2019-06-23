import sqlite3
import os

BOOKS_PATH = '/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/'

class Book:
    'A book containing fields present in Apple\'s Books app'

    books = 0
    def __init__(self, title, path, author, book_desc, is_new, genre, percent_complete):
        self.title = title
        self.path = path
        self.author = author
        self.book_desc = book_desc if book_desc else "No book description for this title available in Books"
        self.is_new = is_new
        self.genre = genre if genre else ''
        self.percent_complete = '0%' if not percent_complete else str(percent_complete * 100)[:4] + '%' # str(percent_complete * 100) + "%"
        Book.books += 1

    def display_book(self):
        return {'title:' : self.title,
                'path:' : self.path,
                'author:' : self.author,
                'book_desc:' : self.book_desc,
                'is_new:' : self.is_new,
               }

    def display_count(self):
        return 'Total books: ' + str(Book.books)

def get_book_db():
    book_dir = os.path.expanduser('~' + BOOKS_PATH)
    dbs = []
    dbs += [each for each in os.listdir(book_dir) if (each.endswith('.sqlite') and each.startswith('BKLibrary')) ]
    db_path = book_dir + dbs[0]
    return db_path

def get_books():
    conn = sqlite3.connect(get_book_db())
    c = conn.cursor()
    c.execute('''SELECT "_rowid_",* FROM "main"."ZBKLIBRARYASSET" ORDER BY "_rowid_" ASC LIMIT 0, 49999;''')
    data = c.fetchall()
    books = []
    for b in data:
        # check if path exists
        if (b[72]):
            books.append(Book(b[78],b[72],b[56],b[57],b[18],b[66],b[50]))
    conn.close()
    return books

def get_one_book():
    conn = sqlite3.connect(get_book_db())
    c = conn.cursor()
    c.execute('''SELECT "_rowid_",* FROM "main"."ZBKLIBRARYASSET" ORDER BY "_rowid_" ASC LIMIT 0, 49999;''')
    data = c.fetchone()
    count = 0
    for d in data:
        print(str(count) + ": " + str(d))
        count+=1
    conn.close()
    return

# get_one_book()

# count = 0 
# b = get_books()
# for t in range(0, len(b)):
#     print(str(count) + ": " + str(b[count]))
#     count += 1

# books = get_books()
# print(books[-1].display_count())
# for b in books:
#     print(b.title)
