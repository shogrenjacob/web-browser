
def showHeaders(headers):
    for header in headers:
        print(header)

def print_tree(node, indent=0):
    print(" " * indent, node)
    for child in node.children:
        print_tree(child, indent + 2)

