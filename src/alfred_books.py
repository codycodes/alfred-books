# encoding: utf-8
from __future__ import unicode_literals

import sys
import book
from workflow import Workflow, ICON_WARNING, ICON_INFO, MATCH_ALL, \
    MATCH_ALLCHARS

log = None


def main(wf):

    if wf.update_available:
        # Adds a notification to top of Script Filter results
        wf.add_item('New version available',
                    'Action this item to install the update',
                    valid=False,
                    autocomplete='workflow:update',
                    icon=ICON_INFO)

    args = len(wf.args)

    option = None
    if args and wf.args[0]:
        switch = wf.args[0].split()[0]
        switches = [u'-a', u'-t', u'-g', u'-h', u'-n']
        if any([switch in switches]):
            switch = switch[:2]
            query, option = wf.args[0].split(switch)[1], switch
        else:
            query, option = wf.args[0], None

    else:
        query = None
    books = wf.cached_data('books', book.get_books, max_age=5)

    # Don't do anything else if there are no books
    if not books:
        wf.add_item('No books found. Check the Books app first.',
                    icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    # show help with no space required
    if query or option == '-h':
        if option:
            if option == '-a':
                books = wf.filter(
                    query,
                    books,
                    key=lambda book: book.author,
                    match_on=MATCH_ALL ^ MATCH_ALLCHARS, min_score=30
                )
            elif option == '-t':
                books = wf.filter(
                    query,
                    books,
                    key=lambda book: book.title,
                    match_on=MATCH_ALL ^ MATCH_ALLCHARS, min_score=30
                )
            elif option == '-g':
                books = wf.filter(
                    query,
                    books,
                    key=lambda book: book.genre,
                    match_on=MATCH_ALL ^ MATCH_ALLCHARS, min_score=30
                )
            elif option == '-h':
                wf.add_item(
                    title='alfred-books options:',
                    subtitle='-t search via title, ' +
                    '-a search via author, ' +
                    '-g search via genre, ' +
                    '-h show switches',
                    largetext='-t   search via title,\n' +
                    '-a  search via author,\n' +
                    '-g  search via genre,\n' +
                    '-n "True/False" filters to show new books or not,\n'
                    '-h  show switches (this one),\n' +
                    'no option(s)  search by title and author'
                )
            elif option == '-n':
                books = wf.filter(
                    query,
                    books,
                    key=lambda book: book.is_new,
                    match_on=MATCH_ALL ^ MATCH_ALLCHARS, min_score=30
                )
        else:
            books = wf.filter(
                query,
                books,
                key=lambda book: book.title + book.author,
                match_on=MATCH_ALL ^ MATCH_ALLCHARS, min_score=30
            )

    books.sort(key=lambda book: book.last_accessed, reverse=True)
    for b in books:
        wf.add_item(type='file',
                    title=b.title,
                    valid=True,
                    subtitle=b.author if b.path is not None else
                    'Please download file in books app first'
                    ' to open in Alfred Books',
                    arg=b.path,
                    icon=b.path,
                    icontype='fileicon',
                    quicklookurl=b.path,
                    largetext=b.title + ', by ' + b.author +
                    '\nIs new: ' + b.is_new +
                    '\nGenre: ' + b.genre +
                    '\nCompleted: ' + b.read_pct +
                    '\nDescription:\n' + b.book_desc)
    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow(help_url='https://github.com/codycodes/alfred-books/issues',
                  update_settings={'github_slug': 'codycodes/alfred-books'})
    log = wf.logger
    sys.exit(wf.run(main))
