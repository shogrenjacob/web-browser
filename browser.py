import tkinter
import tkinter.font

from collections import deque

from displayHtml import HtmlParser, showHTML
from debug import print_tree
from url import URL
from globals import HSTEP, VSTEP, WIDTH, HEIGHT
from layout import Layout
from BlockLayout import paint_tree, BlockLayout
from DocumentLayout import DocumentLayout

#TODO: Fix bug where, when displaying cached page, after resizing, the browser draws the most recently requested body

class Browser:
    def __init__(self):
        self.SCROLL_STEP = 100

        self.window = tkinter.Tk()
        self.window.title("Jacob's Web Browser :)")

        self.cache = {}

        self.prev_page_stack = deque()
        self.next_page_stack = deque()

        def search():
            search_query = self.search_bar.get()

            # if search_query in self.cache:
            #     self.canvas.delete("all")
            #     self.scroll = 1
            #     self.display_list = Layout(self.cache[search_query])
            #     self.draw()
            #     print("Loaded from Cache")

            url = URL(search_query)
            self.canvas.delete("all")
            self.scroll = 1
            print("loading from request")

            self.current_page = url
            self.prev_page_stack.append(url)
            self.load(url)
        
        def return_to_prev():
            self.next_page_stack.append(self.current_page)

            if len(self.prev_page_stack) != 0:
                print(f"Page stack: {self.prev_page_stack}")
                prev_page = self.prev_page_stack.pop()

                if prev_page == self.current_page:
                    prev_page = self.prev_page_stack.pop()

                print(f"Prev Page: {prev_page}")
                self.current_page = prev_page
                self.load(prev_page)
        
        def to_next_page():
            if len(self.next_page_stack) != 0:
                self.prev_page_stack.append(self.current_page)
                next_page = self.next_page_stack.pop()

                self.current_page = next_page
                self.load(next_page)
            else:
                print("next page stack empty")
        
        self.top_frame = tkinter.Frame(self.window)
        self.top_frame.pack(side=tkinter.TOP, fill=tkinter.X)

        self.return_button = tkinter.Button(self.top_frame, text="<-", command=return_to_prev, bg="white")
        self.return_button.pack(side="left", expand=True)
        self.next_button = tkinter.Button(self.top_frame, text="->", command=to_next_page, bg="white")
        self.next_button.pack(side="left", expand=True)
        self.search_bar = tkinter.Entry(self.top_frame, width=100)
        self.search_bar.pack(side="left", expand=True)
        self.search_button = tkinter.Button(self.top_frame, text="search", command=search, bg="white")
        self.search_button.pack(side="left", padx=(10,0), expand=True)

        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT, bd=2, relief="solid")
        self.canvas.pack(side="top")

        self.scroll = 1
        self.display_list = []
        self.text = ""
        self.content_end = 0

        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<MouseWheel>", self.scrollmouse)
        self.window.bind("<Configure>", self.resize)

    def load(self, url: URL):
        
        self.url = url

        # Add to cache if new request
        if self.url not in self.cache:
            body = url.request()
        else:
            body = self.cache[self.url]

        # Show html instead of content if view-source is requested
        if url.subscheme == "view-source":
            self.nodes = HtmlParser(body).parse()
            print_tree(self.nodes)
        else:
            self.nodes = HtmlParser(body).parse()
        
        # Add new request to cache
        self.cache[self.url.name] = self.text

        self.document = DocumentLayout(self.nodes)
        self.document.layout()
        self.display_list = []
        paint_tree(self.document, self.display_list)
        self.content_end = self.document.height
        self.draw()
    
    def draw(self):
        self.canvas.delete("all")

        for cmd in self.display_list:
            if cmd.top > self.scroll + HEIGHT: continue
            if cmd.bottom < self.scroll: continue
            cmd.execute(self.scroll, self.canvas)

    # e denotes the keyup event
    def scrolldown(self, e):
        if self.scroll >= self.content_end - HEIGHT:
            self.scroll = self.content_end - HEIGHT - 1
        else:
            self.canvas.delete("all")
            self.scroll += self.SCROLL_STEP
            self.draw()

    def scrollup(self, e):
        if self.scroll <= 0:
            self.scroll = 1
        else:
            self.canvas.delete("all")
            self.scroll -= self.SCROLL_STEP
            self.draw()

    def scrollmouse(self, e):
        if self.scroll > 0 and self.scroll < self.content_end - HEIGHT:
            self.canvas.delete("all")

            self.scroll -= e.delta * (self.SCROLL_STEP / 2)

            if self.scroll <= 0:
                self.scroll = 1
            elif self.scroll >= self.content_end - HEIGHT:
                self.scroll = self.content_end - HEIGHT - 1

            self.draw()
        elif self.scroll <= 0:
            self.scroll = 1
        elif self.scroll >= self.content_end - HEIGHT:
            self.scroll = self.content_end - HEIGHT - 1
        
    def resize(self, e):
        global WIDTH, HEIGHT
        WIDTH = e.width
        HEIGHT = e.height
        self.canvas.pack(fill='both', expand=1)

        if self.content_end != 0:
            self.canvas.delete("all")

            self.document = DocumentLayout(self.nodes)
            self.document.layout()
            self.display_list = []
            paint_tree(self.document, self.display_list)
            self.content_end = self.document.height
            
            self.draw()

