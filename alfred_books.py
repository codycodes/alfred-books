import sys
import book
from workflow import Workflow, ICON_WEB, web
import logging

__version__ = '0.1'
log = None

def main(wf):

    log.debug('Started')
    # check if there's a query
    args = len(wf.args)
    log.debug('ARGS: ' + str(wf.args))
    if args:
        switch = wf.args[0]
        if '-a' or '-t' or '-n' in switch:
            switch = switch[:2]
            # log.debug('!!found options!!' +  wf.args[0].split(switch)[1])
            query, option = wf.args[0].split(switch)[1], switch
        else:   
            query, option = wf.args[0], None
    else:
        query = None

    books = book.get_books()

    # log.debug('OPTION: ' + str(option))
    # TODO: play around with the text matching.
    if query:
        if option:
            if option == '-a':
                books = wf.filter(query, books, key=lambda book: u' '.join(book.author), min_score=30)
            elif option == '-t':
                books = wf.filter(query, books, key=lambda book: u' '.join(book.title), min_score=30)
            elif option == '-n':
                # TODO: add is_new filter
                pass
            else:
                books = wf.filter(query, books, key=lambda book: u' '.join(book.title + u' ' + book.author), min_score=30)
        else:
            books = wf.filter(query, books, key=lambda book: u' '.join(book.title + u' ' + book.author), min_score=30)

    for b in books:
        wf.add_item(type='file',
                    title=b.title, 
                    valid=True,
                    subtitle=b.author,
                    arg=b.path,
                    modifier_subtitles={'cmd' : b.path},
                    quicklookurl=b.path,
                    )
    wf.send_feedback()



if __name__ == u"__main__":
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))