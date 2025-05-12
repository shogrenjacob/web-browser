import tkinter
from displayHtml import lex, showHTML
from url import URL

class Browser:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.HSTEP, self.VSTEP = 13, 18
        self.SCROLL_STEP = 100

        self.window = tkinter.Tk()
        self.window.title("Jacob's Web Browser :)")

        self.canvas = tkinter.Canvas(self.window, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack(side="left")

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
        body = url.request()

        if url.subscheme == "view-source":
            self.text = showHTML(body)
        else:
            self.text = lex(body)

        self.display_list = self.layout(self.text)
        self.draw()
    
    def draw(self):
        for x, y, c in self.display_list:

            # Only create text that needs to be displayed, gets us closer to frame budget
            if y > self.scroll + self.HEIGHT:
                continue
            if y + self.VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c)

    # e denotes the keyup event
    def scrolldown(self, e):
        self.canvas.delete("all")
        self.scroll += self.SCROLL_STEP
        self.draw()

    def scrollup(self, e):
        if self.scroll != 0:
            self.canvas.delete("all")
            self.scroll -= self.SCROLL_STEP
            self.draw()

    def scrollmouse(self, e):
        if self.scroll > 0 and self.scroll < self.content_end - self.HEIGHT:
            self.canvas.delete("all")

            self.scroll -= e.delta * (self.SCROLL_STEP / 2)

            if self.scroll <= 0:
                self.scroll = 1
            elif self.scroll >= self.content_end - self.HEIGHT:
                self.scroll = self.content_end - self.HEIGHT - 1

            self.draw()
        elif self.scroll <= 0:
            self.scroll = 1
        elif self.scroll >= self.content_end - self.HEIGHT:
            self.scroll = self.content_end - self.HEIGHT - 1
        print(self.scroll)
        
    def resize(self, e):
        self.WIDTH = e.width
        self.HEIGHT = e.height
        self.canvas.pack(fill='both', expand=1)

        self.canvas.delete("all")
        self.layout(self.text)
        self.draw()


    def layout(self, text):
        self.display_list = []
        cursor_x, cursor_y = self.HSTEP, self.VSTEP

        for c in text:
            if c == '\n':
                cursor_y += self.VSTEP + 8
                cursor_x = self.HSTEP
                continue

            self.display_list.append((cursor_x, cursor_y, c))
            
            if cursor_x >= self.WIDTH - self.HSTEP:
                cursor_y += self.VSTEP
                cursor_x = self.HSTEP
            else:    
                cursor_x += self.HSTEP
        self.content_end = cursor_y
        print(self.content_end)
        return self.display_list

