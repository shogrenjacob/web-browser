import tkinter
import tkinter.font
from displayHtml import Text, Tag

HSTEP, VSTEP = 13, 18
WIDTH, HEIGHT = 800, 600

class Layout:
    def __init__(self, tokens):
        self.display_list = []

        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"

        for tok in tokens:
            self.token(tok)
    
    def token(self, tok):
        if isinstance(tok, Text):
            for word in tok.text.split():
                self.word(word)
        elif tok.tag == "i":
            style = "italic"
        elif tok.tag == "/i":
            style = "roman"
        elif tok.tag == "b":
            weight = "bold"
        elif tok.tag == "/b":
            weight = "normal"

    def word(self, word):
        font = tkinter.font.Font(size=16, weight=self.weight, slant=self.style)

        w = font.measure(word)
        # if word == '\n':
        #     cursor_y += self.VSTEP + 8
        #     cursor_x = self.HSTEP
        #     continue

        self.display_list.append((self.cursor_x, self.cursor_y, word, font))
        self.cursor_x += w + font.measure(" ")
                    
        if self.cursor_x + w >= WIDTH - HSTEP:
            self.cursor_y += font.metrics("linespace") * 1.25
            self.cursor_x = HSTEP
        else:    
            self.cursor_x += HSTEP