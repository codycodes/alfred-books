import sys
import book
from workflow import Workflow, ICON_WEB, web, Variables
import logging

__version__ = '0.1'
log = None


def main(wf):

    log.debug('Started')
    args = len(wf.args)
    log.debug('ARGS: ' + str(wf.args))

    option = None
    if args and wf.args[0]:
        switch = wf.args[0]
        if '-a' or '-t' or '-h' in switch:
            switch = switch[:2]
            query, option = wf.args[0].split(switch)[1], switch
        else:   
            query, option = wf.args[0], None
    else:
        query = None
    # max age of 20 seconds to reduce querying database
    # and make it blazingly fast
    books = wf.cached_data('books', book.get_books, max_age=20)

    # log.debug('OPTION: ' + str(option))
    # TODO: play around with the text matching.
    # show help with no space required
    if query or option == '-h':
        if option:
            if option == '-a':
                books = wf.filter(query, books, key=lambda book: u' '.join(book.author), min_score=30)
            elif option == '-t':
                books = wf.filter(query, books, key=lambda book: u' '.join(book.title), min_score=30)
            elif option == '-h':
                wf.add_item(
                    title='alfred-books options:',
                    subtitle='-t search via title, -a search via author, -h show switches',
                    largetext="-t   search via title,\n-a  search via author,\n-h  show switches (this one)"
                )

    for b in books:
        wf.add_item(type='file',
                    title=b.title, 
                    valid=True,
                    subtitle=b.author,
                    arg=b.path,
                    quicklookurl=b.path,
                    largetext=b.book_desc,
                    )
    wf.send_feedback()



if __name__ == u"__main__":
    wf = Workflow(help_url='https://github.com/codycodes/alfred-books')
    log = wf.logger
    sys.exit(wf.run(main))