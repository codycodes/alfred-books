# encoding: utf-8
from __future__ import unicode_literals
import sqlite3
import os

BOOKS_PATH = os.path.expanduser(
    '~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/')


class Book:
    'A book containing fields present in Apple\'s Books app'

    books = 0

    def __init__(self, title, path, author, book_desc, is_new, genre,
                 read_pct, last_accessed):
        self.title = title
        self.path = path
        self.author = author
        self.book_desc = book_desc if book_desc \
            else "No book description for this title available in Books"
        self.is_new = "True" if is_new else "False"
        self.genre = genre if genre else 'No genre for this title available in Books'
        self.read_pct = '0%' if not read_pct else str(read_pct * 100)[:4] + '%'
        self.last_accessed = last_accessed
        Book.books += 1

    def display_book(self):
        return {
            'title:': self.title,
            'path:': self.path,
            'author:': self.author,
            'book_desc:': self.book_desc,
            'is_new:': self.is_new,
        }

    def display_count(self):
        return 'Total books: ' + str(Book.books)


def get_book_db():
    dbs = []
    dbs += [each for each in os.listdir(BOOKS_PATH)
            if (each.endswith('.sqlite') and each.startswith('BKLibrary'))]
    db_path = BOOKS_PATH + dbs[0]
    return db_path


def get_books():
    conn = sqlite3.connect(get_book_db())
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''SELECT "_rowid_",* FROM "main"."ZBKLIBRARYASSET" ORDER BY "_rowid_" ASC LIMIT 0, 49999;''')
    data = c.fetchall()
    books = []
    for row in data:
        row = dict(row)
        # check if path exists
        if row['ZPATH'] is not None:
            if os.path.exists(row['ZPATH']):
                try:
                    # grab last metadata change
                    last_accessed = float(os.stat(row['ZPATH']).st_ctime)
                except OSError:
                    # inaccessible path
                    last_accessed = -1
            else:
                # book not downloaded
                last_accessed = -1

            book = Book(
                title=row['ZTITLE'],
                path=row['ZPATH'] if os.path.exists(row['ZPATH']) else None,
                author=row['ZAUTHOR'],
                book_desc=row['ZBOOKDESCRIPTION'],
                is_new=row['ZISNEW'],
                genre=row['ZGENRE'],
                read_pct=row['ZREADINGPROGRESS'],
                last_accessed=last_accessed,
            )
            books.append(book)
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
        count += 1
    conn.close()
    return
