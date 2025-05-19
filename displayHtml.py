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
        showHTML(body)
    else:
        HtmlParser.parse(body)