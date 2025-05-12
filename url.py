import socket
import ssl
from debug import showHeaders

class URL:
    def __init__(self, url: str):
        self.subscheme = ""
        self.valid_scehemes = ["http", "https", "file", "view-source:http", "view-source:https"]
        self.name = url

        if "://" in url:
            self.scheme, url = url.split("://", 1)
            if self.scheme not in self.valid_scehemes:
                self.scheme = "blank"
                self.subscheme = "about"                
        elif "://" not in url:
            self.scheme = "blank"
            self.subscheme = "about"
        

        if self.scheme == "http" or self.scheme == "view-source:http":
            self.port = 80
            if self.scheme == "view-source:http":
                self.subscheme, self.scheme = self.scheme.split(":", 1)
                print("scheme: " + self.scheme)
                print("subscheme: " + self.subscheme)
        elif self.scheme == "https" or self.scheme == "view-source:https":
            self.port = 443
            if self.scheme == "view-source:https":
                self.subscheme, self.scheme = self.scheme.split(":", 1)
                print("scheme: " + self.scheme)
                print("subscheme: " + self.subscheme)
        elif self.scheme == "file":
            self.port = 0
        if self.scheme == "blank":
            self.port = 0

        if "/" not in url:
            url = url + "/"

        self.host, url = url.split("/", 1)
        self.path = "/" + url

        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

        self.content_length = ""
    
    def request(self):

        if self.scheme == "file":
            file = open(self.path, 'r')
            content = file.read()
            file.close()
            return content
        elif self.scheme == "blank":
            content = "about:blank"
            return content
        else:
            ctx = ssl.create_default_context()

            # Create a socket with INET address family, Stream socket type, and use TCP
            s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
            s.connect((self.host, self.port))

            if self.scheme == "https":
                ctx = ssl.create_default_context()
                s = ctx.wrap_socket(s, server_hostname=self.host)

            headers = [
                "GET {} HTTP/1.0".format(self.path),
                "Host: {}".format(self.host),
                "Connection: close",
                "User-Agent: Jacob's Browser!",
            ]

            for header in headers:
                if header == headers[0]:
                    request = header + "\r\n"
                else:
                    request += header + "\r\n"

            request += "\r\n"

            s.send(request.encode("utf8"))

            # Makefile returns a file-like object containing every byte we receive from server
            response = s.makefile("r", encoding="utf8", newline="\r\n")

            status_line = response.readline()
            version, status, explaination = status_line.split(" ", 2)
            print("version: " + version + "\n" + "status: " + status + "\n" + "explaination: " + explaination + "\n")

            response_headers = {}

            # For each response header, add to the response_headers dict, make headers lowercase and strip values of whitespace
            while True:
                line = response.readline()
                if line == "\r\n":
                    break
                header, value = line.split(":", 1)
                response_headers[header.casefold()] = value.strip()

            # Make sure unusually encoded data isn't being sent
            assert "transfer-encoding" not in response_headers
            assert "content-encoding" not in response_headers

            self.content_length = response_headers["content-length"]

            print(response_headers)

            if 299 < int(status) < 400:
                self.redirect = response_headers["location"]

                if "://" not in self.redirect:
                    self.redirect = self.scheme + "://" + self.host + self.redirect
                    print("self.redirect: " + self.redirect)

                new_url = URL(self.redirect)
                new_url.request()
                self.content = new_url.content
                return self.content
            
            # Now, get everything after the headers
            self.content = response.read()
            s.close()

            return self.content