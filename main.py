import tkinter
import sys

from browser import Browser
from url import URL
from displayHtml import load
from HtmlParser import HtmlParser
from debug import print_tree

if __name__ == "__main__":    

    # pretty print the DOM with -t flag for debugging
    # if sys.argv:
    #     if sys.argv[2] == "-t":
    #         body = URL(sys.argv[1]).request()
    #         nodes = HtmlParser(body).parse()
    #         print_tree(nodes)
    Browser()
    tkinter.mainloop()