import sys
import book
from workflow import Workflow, ICON_WARNING, ICON_INFO, MATCH_ALL, \
    MATCH_ALLCHARS

log = None


def main(wf):

    log.debug('Started')

    if wf.update_available:
        # Adds a notification to top of Script Filter results
        wf.add_item('New version available',
                    'Action this item to install the update',
                    valid=False,
                    autocomplete='workflow:update',
                    icon=ICON_INFO)

    args = len(wf.args)
    log.debug('ARGS: ' + str(wf.args))

    option = None
    if args and wf.args[0]:
        switch = wf.args[0].split()[0]
        # log.debug('SWITCH: ' + switch)
        switches = [u'-a', u'-t', u'-g', u'-h']
        if any([switch in switches]):
            switch = switch[:2]
            log.debug('SWITCH: ' + switch)
            query, option = wf.args[0].split(switch)[1], switch
        else:
            query, option = wf.args[0], None
    else:
        query = None
    # max age of 20 seconds to reduce querying database
    # and make it blazingly fast
    books = wf.cached_data('books', book.get_books, max_age=20)
    # books = book.get_books()

    # Don't do anything else if there are no books
    if not books:
        wf.add_item('No books found. Check the Books app first.',
                    icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    log.debug('QUERY: ' + str(query) + ', OPTION: ' + str(option))

    # show help with no space required
    if query or option == '-h':
        if option:
            if option == '-a':
                log.debug('-a input')
                books = wf.filter(
                    query,
                    books,
                    key=lambda book: u' '.join(book.author),
                    match_on=MATCH_ALL ^ MATCH_ALLCHARS, min_score=30
                )
            elif option == '-t':
                log.debug('-t input')
                books = wf.filter(
                    query,
                    books,
                    key=lambda book: u' '.join(book.title),
                    match_on=MATCH_ALL ^ MATCH_ALLCHARS, min_score=30
                )
            elif option == '-g':
                log.debug('-g input')
                books = wf.filter(
                    query,
                    books,
                    key=lambda book: u' '.join(book.genre),
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
                    '-h  show switches (this one),\n' +
                    'no option(s)  search by title and author'
                )
        else:
            books = wf.filter(
                query,
                books,
                key=lambda book: u' '.join(book.title) + u' ' +
                u' '.join(book.author),
                match_on=MATCH_ALL ^ MATCH_ALLCHARS, min_score=30
            )

    for b in books:
        if b.genre == '':
            b.genre = 'No genre for this title available in Books'
        wf.add_item(type='file',
                    title=b.title,
                    valid=True,
                    subtitle=b.author,
                    arg=b.path,
                    icon=b.path,
                    icontype='fileicon',
                    quicklookurl=b.path,
                    largetext=b.title + u', by ' + b.author +
                    u'\nGenre: ' + b.genre +
                    u'\nCompleted: ' + b.read_pct +
                    u'\nDescription:\n' + b.book_desc)
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow(help_url='https://github.com/codycodes/alfred-books/issues',
                  update_settings={'github_slug': 'codycodes/alfred-books'})
    log = wf.logger
    sys.exit(wf.run(main))
