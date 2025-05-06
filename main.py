import tkinter

from browser import Browser
from url import URL
from displayHtml import load

if __name__ == "__main__":
    import sys

    # Set default path in case of no given path to parse
    default_path = "file:///Users/jacobshogren/Code/python/web-browser/test.html"

    if len(sys.argv) < 2:
        Browser().load(URL(default_path))
        tkinter.mainloop()
    else:
        Browser().load(URL(sys.argv[1]))
        tkinter.mainloop()