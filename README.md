# Jacob's Web Browser!

This project is based off of the principles and designs found in the chapters and exercises of [Web Browser Engineering](https://browser.engineering/).
This book provides the foundation to create a usable web browser written in Python. 

## How to Run
Clone this repo or download this source code. Once its downloaded, you can run the following command to start up the browser:

```bash 
python3 main.py # Mac
python main.py # Windows
```

This will bring up your browser window, where you can type in a url and hit search. Doing so will return the content for the requested webpage.

## Features
- Basic browsing capabilities, displays the content for a requested webpage.
- A "Return to Previous Page" button.
- View local files with the "file://" scheme
- Support for the view-source subscheme.
- Supports HTTP and HTTPS.
- HTTP Request logging (Viewable in terminal)

## How It's Made
I made this project using Python and Tkinter, utilizing an Object-Oriented approach to build my browser. In this project I implemented several components used in modern browser such as
an HTML parser, HTML and layout trees, a webpage cache, classes for drawing HTML to the window, and a basic GUI.

## Optimization
Drawing HTML to the window can be expensive, so I implemented multiple optimizations to speed up the process and to give the user a quicker browsing experience.
1. Conditional HTML drawing - My browser first measures the amount of space needed for the content on the webpage. If the content height is greater than the window height,
it will only draw the content that fits in the window.
2. Webpage Cache - When a webpage is requested for the first time, a copy of the full HTML tree is saved in a cache. Whenever the webpage is requested again, it is loaded
from cache rather than an HTTP request, reducing load times significantly.
3. Webpage Layout Caching - Another cache for storing attributes like font, font-size, font-weight, and font-style for each HTML element in the tree. This reduces the amount of time
needed for the browser to draw the content.

## Change Log
- June 15, 2025: Version 1.0