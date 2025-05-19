import tkinter
import tkinter.font
from displayHtml import displayEncoded
from HtmlParser import Text, Element
from globals import HSTEP, VSTEP, HEIGHT, WIDTH, FONTS

class Layout:
    def __init__(self, tree):
        self.display_list = []

        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.size = 16
        self.line = []

        self.font = tkinter.font.Font(size=self.size, weight=self.weight, slant=self.style)

        self.recurse(tree)

        self.flush()
    
    def open_tag(self, tag):
        if tag == "i":
            self.style = "italic"
        
    def close_tag(self, tag):
        if tag == "i":
            self.style = "roman"

    # Traverse the node tree
    def recurse(self, tree):
        if isinstance(tree, Text):
            for word in tree.text.split():
                self.word(word)
        else:
            self.open_tag(tree.tag)
            for child in tree.children:
                self.recurse(child)
            
            self.close_tag(tree.tag)
    
    def token(self, tok):
        if isinstance(tok, Text):
            if tok.text == "\n":
                self.cursor_y += VSTEP
            elif tok.text[0] == "&" and tok.text[1] != " ":
                decodedChars = displayEncoded(tok.text)
                for char in decodedChars:
                    self.word(char)
            else:
                for word in tok.text.split():
                    self.word(word)
        elif tok.tag == "i":
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            self.weight = "bold"
        elif tok.tag == "/b":
            self.weight = "normal"
        elif tok.tag == "small":
            self.size -= 2
        elif tok.tag == "/small":
            self.size += 2
        elif tok.tag == "big":
            self.size += 4
        elif tok.tag == "/big":
            self.size -= 4
        elif tok.tag == "br":
            self.flush()
        elif tok.tag == "/p":
            self.flush()
            self.cursor_y += VSTEP

    def word(self, word):
        self.font = self.get_font(self.size, self.weight, self.style)
        w = self.font.measure(word)
                    
        if self.cursor_x + w >= WIDTH - HSTEP:
            self.flush()
            self.cursor_y += self.font.metrics("linespace") * 1.25
            self.cursor_x = HSTEP

        self.line.append((self.cursor_x, word, self.font))
        self.cursor_x += w + self.font.measure(" ")
        
    
    def flush(self):
        if not self.line: return

        metrics = [self.font.metrics() for x, word, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])

        baseline = self.cursor_y + 1.25 * max_ascent

        for x, word, font in self.line:
            y = baseline - self.font.metrics("ascent")
            self.display_list.append((x, y, word, font))

        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + 1.25 * max_descent

        self.cursor_x = HSTEP
        self.line = []

    def get_font(self, size, weight, style):
        key = (size, weight, style)

        if key not in FONTS:
            self.font = tkinter.font.Font(size=size, weight=weight, slant=style)
            label = tkinter.Label(font=self.font)
            FONTS[key] = (self.font, label)
        
        return FONTS[key][0]