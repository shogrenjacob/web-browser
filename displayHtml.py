from url import URL

class Text:
    def __init__(self, text):
        self.text = text

class Tag:
    def __init__(self, text):
        self.tag = text

def lex(body):
    out = []
    buffer = ""
    in_tag = False

    for c in body:
        if c == "<":
            in_tag = True
            if buffer:
                out.append(Text(buffer))
            buffer = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(buffer))
            buffer = ""
        else:
            buffer += c
    
    if not in_tag and buffer:
        out.append(Text(buffer))
    
    return out

def showHTML(body):
    text = ""
    for c in body:
        text += c
    return text

def load(url: URL):
    body = url.request()
    if url.subscheme == "view-source":
        print("in load, url scheme: " + url.scheme)
        showHTML(body)
    else:
        print("using lex")
        lex(body)
