import tkinter
import tkinter.font
import html

from HtmlParser import Text, Element
from globals import HSTEP, VSTEP, HEIGHT, WIDTH, FONTS, CURSOR_X, CURSOR_Y, BLOCK_ELEMENTS

class BlockLayout:
    def __init__(self, node, parent, previous):
        self.node = node
        self.parent = None
        self.previous = previous
        self.children = []
        

    def layout(self):
        mode = self.layout_mode()

        if mode == "block":
            previous = None

            for child in self.node.children:
                next = BlockLayout(child, self, previous)
                self.children.append(next)
                previous = next
        else:
            self.cursor_x = 0
            self.cursor_y = 0
            self.weight = "normal"
            self.style = "roman"
            self.size = 12

            self.line = []
            self.recurse(self.node)
            self.flush()

        for child in self.children:
            child.layout()

    def open_tag(self, tag):
        global CURSOR_X, CURSOR_Y
        if tag == "i":
            self.style = "italic"
        if tag == "b":
            self.weight = "bold"
        if tag == "small":
            self.size = 12
        if tag == "big":
            self.size = 20
        if tag == "p":
            self.flush()
            CURSOR_Y += VSTEP * 2
        if tag == "br":
            self.flush()
            CURSOR_Y += VSTEP * 5
        if tag == "li":
            self.flush()
            CURSOR_X += HSTEP * 2
        if tag == "ul" or tag == "ol":
            self.flush()
        
    def close_tag(self, tag: str):
        if tag == "i":
            self.style = "roman"
        if tag == "b":
            self.weight = "normal"
        if tag == "small" or tag == "big":
            self.size = 16



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

    def word(self, word):
        global CURSOR_Y, CURSOR_X
        word = html.unescape(word)

        self.font = self.get_font(self.size, self.weight, self.style)
        w = self.font.measure(word)
                    
        if CURSOR_X >= WIDTH: # removed + w from CURSOR_X +w and - HSTEP from WIDTH - HSTEP
            self.flush()
            CURSOR_Y += self.font.metrics("linespace") * 1.25
            CURSOR_X = HSTEP

        self.line.append((CURSOR_X, word, self.font))
        CURSOR_X += w + self.font.measure(" ")
        
    
    def flush(self):
        global CURSOR_X, CURSOR_Y
        if not self.line: return

        metrics = [self.font.metrics() for x, word, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])

        baseline = CURSOR_Y + 1.25 * max_ascent

        for x, word, font in self.line:
            y = baseline - self.font.metrics("ascent")
            self.display_list.append((x, y, word, font))

        max_descent = max([metric["descent"] for metric in metrics])
        CURSOR_Y = baseline + 1.25 * max_descent

        CURSOR_X = HSTEP
        self.line = []

    def get_font(self, size, weight, style):
        key = (size, weight, style)

        if key not in FONTS:
            self.font = tkinter.font.Font(size=size, weight=weight, slant=style)
            label = tkinter.Label(font=self.font)
            FONTS[key] = (self.font, label)
        
        return FONTS[key][0]

    def layout_intermediate(self):
        previous = None

        for child in self.node.children:
            next = BlockLayout(child, self, previous)
            self.children.append(next)
            previous = next

    # Determine whether to use layout_intermediate or recurse, use layout_i if the node is block content, recurse if its text content
    def layout_mode(self):
        if isinstance(self.node, Text):
            return "inline"
        # Error case where a block element also contains a inline element within (ex: <p> this is <b>bold</b></p>)
        elif any([isinstance(child, Element) and child.tag in BLOCK_ELEMENTS for child in self.node.children]):
            return "block"
        elif self.node.children:
            return "inline"
        else:
            return "block"
