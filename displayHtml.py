from url import URL

def lex(body):
    text = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            text += c

    return text

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
