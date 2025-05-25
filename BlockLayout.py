import tkinter
import tkinter.font
import html

from HtmlParser import Text, Element
from globals import HSTEP, VSTEP, HEIGHT, WIDTH, FONTS, BLOCK_ELEMENTS
from DrawItems import DrawRect, DrawText

class BlockLayout:
    def __init__(self, node, parent, previous):
        self.node = node
        self.parent = parent
        self.previous = previous
        self.children = []
        self.x = None
        self.y = None
        self.width = None
        self.height = None
        self.display_list = []
        

    def layout(self):
        self.x = self.parent.x
        self.width = self.parent.width

        if self.previous:
            self.y = self.previous.y + self.previous.height
        else:
            self.y = self.parent.y

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

        if mode == "block":
            self.height = sum([child.height for child in self.children]) # Gets the height of a parent element, needs to be at least sum of all children
        else:
            self.height = self.cursor_y

    def open_tag(self, tag):
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
            self.cursor_y += VSTEP * 2
        if tag == "br":
            self.flush()
            self.cursor_y += VSTEP * 5
        if tag == "li":
            self.flush()
            self.cursor_x += HSTEP * 2
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
        word = html.unescape(word)

        self.font = self.get_font(self.size, self.weight, self.style)
        w = self.font.measure(word)
                    
        if self.cursor_x + w > self.width:
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

        for rel_x, word, font in self.line:
            x = self.x + rel_x
            y = self.y + baseline - self.font.metrics("ascent")
            self.display_list.append((x, y, word, font))

        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + 1.25 * max_descent

        self.cursor_x = HSTEP
        self.cursor_x = 0 # May need to replace above line with this
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
    
    def paint(self):
        cmds = []
        if isinstance(self.node, Element) and self.node.tag == "pre":
            x2, y2 = self.x + self.width, self.y + self.height
            rect = DrawRect(self.x, self.y, x2, y2, "gray")
            cmds.append(rect)
        if self.layout_mode() == "inline":
            for x, y, word, font in self.display_list:
                cmds.append(DrawText(x, y, word, font))
        return cmds

def paint_tree(layout_object, display_list):
    display_list.extend(layout_object.paint())

    for child in layout_object.children:
        paint_tree(child, display_list)