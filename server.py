import socketserver
import os
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime

PORT = int(os.getenv("PORT", 8000))
print(f"PORT={PORT}")


def get_page(query):
    path, qs = query.split("?") if '?' in query else [query, ""]
    path = path.rstrip('/')

    switcher = {
        "/hello": get_page_hello,
        "/goodbye": get_page_goodbye,
    }

    return switcher[path](qs) if path in switcher else "Unknown page!"


def get_page_hello(qs):
    qs = parse_qs(qs) if qs != "" else ""   # return dict
    name = get_name(qs)
    year = get_year(qs)
    return f"""
                    Hey {name}! 
                    You were born in {year}.
                """


def get_page_goodbye(qs):
    return f"""
                    {say_bye(datetime.today().hour)}
                    Time: {datetime.today()}
                 """


def get_name(qs):
    if "name" in qs:
        return qs["name"][0]
    else:
        return "Dude"


def get_year(qs):
    if "age" in qs:
        today = datetime.today().year
        age = int(qs["age"][0])
        return str(today - age)
    else:
        return "Unknown"


def say_bye(hour):
    if hour < 6:
        return "Goodnight!"
    elif hour < 12:
        return "Good Morning!"
    elif hour < 18:
        return "Have a nice day!"
    elif hour < 23:
        return "Good Evening!"
    else:
        return "Goodnight!"


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != "":

            msg = get_page(self.path)

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