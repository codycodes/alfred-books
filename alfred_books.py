import sys
import book
from workflow import Workflow, ICON_WEB, web

def main(wf):
    books = book.get_books()
    for b in books:
        wf.add_item(type='file',
                    title=b.title, 
                    valid=True,
                    subtitle=b.author,
                    arg=b.path,
                    modifier_subtitles={'cmd' : b.path},
                    quicklookurl=b.path,
                    )
    # Workflow.logger(wf)
    wf.send_feedback()

if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))