import tkinter
import tkinter.font
from displayHtml import HtmlParser, showHTML
from debug import print_tree
from url import URL
from globals import HSTEP, VSTEP, WIDTH, HEIGHT
from layout import Layout

#TODO: Fix bug where, when displaying cached page, after resizing, the browser draws the most recently requested body

class Browser:
    def __init__(self):
        self.SCROLL_STEP = 100

        self.window = tkinter.Tk()
        self.window.title("Jacob's Web Browser :)")

        self.cache = {}

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
            self.load(url)
        
        self.top_frame = tkinter.Frame(self.window)
        self.top_frame.pack(side=tkinter.TOP, fill=tkinter.X)

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

        if self.url not in self.cache:
            body = url.request()
        else:
            body = self.cache[self.url]

        if url.subscheme == "view-source":
            self.nodes = HtmlParser(body).parse()
            print_tree(self.nodes)
        else:
            self.nodes = HtmlParser(body).parse()
        
        self.cache[self.url.name] = self.text

        layout = Layout(self.nodes)
        self.display_list = layout.display_list
        self.content_end = layout.cursor_y
        self.draw()
    
    def draw(self):
        for x, y, c, f in self.display_list:

            # Only create text that needs to be displayed, gets us closer to frame budget
            if y > self.scroll + HEIGHT:
                continue
            if y + VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c, font=f, anchor="nw")

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
        WIDTH = e.width
        HEIGHT = e.height
        self.canvas.pack(fill='both', expand=1)

        if self.content_end != 0:
            self.canvas.delete("all")
            Layout(self.nodes)
            self.draw()

