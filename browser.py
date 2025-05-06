import tkinter
from displayHtml import lex, showHTML
from url import URL

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.scroll = 0
        self.display_list = []
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)

    def load(self, url: URL):

        body = url.request()

        if url.subscheme == "view-source":
            print("in load, url scheme: " + url.scheme)
            text = showHTML(body)
        else:
            text = lex(body)

        self.display_list = self.layout(text)
        self.draw()
    
    def draw(self):
        for x, y, c in self.display_list:

            # Only create text that needs to be displayed, gets us closer to frame budget
            if y > self.scroll + HEIGHT:
                continue
            if y + VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c)

    def scrolldown(self, e):
        self.canvas.delete("all")
        self.scroll += SCROLL_STEP
        self.draw()

    def scrollup(self, e):
        self.canvas.delete("all")
        self.scroll -= SCROLL_STEP
        self.draw()    

    def layout(self, text):
        self.display_list = []
        cursor_x, cursor_y = HSTEP, VSTEP

        for c in text:
            self.display_list.append((cursor_x, cursor_y, c))
            if cursor_x >= WIDTH - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP
            else:    
                cursor_x += HSTEP
        return self.display_list

