from BlockLayout import BlockLayout
from globals import WIDTH, HEIGHT, HSTEP, VSTEP

class DocumentLayout:
    def __init__(self, node):
        self.node = node
        self.parent = None
        self.children = []
        self.x = None
        self.y = None
        self.width = None
        self.height = None
    
    def layout(self):
        child = BlockLayout(self.node, self, None)
        self.children.append(child)
        child.layout()

        self.width = WIDTH - 2 * HSTEP
        self.x = HSTEP
        self.y = VSTEP
        child.layout()
        self.height - child.height