import tkinter
import tkinter.font

from url import URL
from HtmlParser import HtmlParser, Text, Element
from globals import FONTS

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
        print("using parser")
        HtmlParser.parse(body)

def displayEncoded(tok: Text):
    encodedList = tok.split(";")
    decodedList = []

    for item in encodedList:
        cleanedItem = item.strip("&")

        if cleanedItem == "lt":
            decodedList.append("<")
        elif cleanedItem == "gt":
            decodedList.append(">")
        elif cleanedItem == "amp":
            decodedList.append("&")
        elif cleanedItem == "quot":
            decodedList.append('"')
        elif cleanedItem == "apos":
            decodedList.append("'")
    

    return decodedList