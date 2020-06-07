import socketserver
import os
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import date

PORT = int(os.getenv("PORT", 8000))
print(f"PORT={PORT}")

def get_name(qs):
    if qs == "":
        return "Dude"
    else:
        qs = parse_qs(qs)  # return dict
        if "name" not in qs:
            return "Dude"
        else:
            return qs["name"][0]

def get_year(qs):
    if qs == "":
        return "Unknown"
    else:
        qs = parse_qs(qs)  # return dict
        if "age" not in qs:
            return "Unknown"
        else:
            today = date.today().year
            return str(today - int(qs["age"][0]))

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/hello"):
            path, qs = self.path.split("?") if '?' in self.path else [self.path, ""]
            name = get_name(qs)
            year = get_year(qs)
            msg = f"""
                        Hey {name}! 
                        You were born in {year}.
                        Your path: {self.path}.
                    """

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(msg))
            self.end_headers()

            self.wfile.write(msg.encode())
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
# httpd = socketserver.TCPServer(("", PORT), MyHandler)
    print("it works")
    httpd.serve_forever()