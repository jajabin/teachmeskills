import socketserver
import os
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime

PORT = int(os.getenv("PORT", 8000))
print(f"PORT={PORT}")

def get_page(query):
    path, qs = query.split("?") if '?' in query else [query, ""]
    if path.startswith("/hello"):
        name = get_name(qs)
        year = get_year(qs)
        return f"""
                    Hey {name}! 
                    You were born in {year}.
                    Your path: {query}.
                """
    elif path.startswith("/goodbye"):
        return f"""
                    {say_bye(datetime.today().hour)}
                    Time: {datetime.today()}
                 """
    else:
        return "Unknown page"

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
            today = datetime.today().year
            age = int(qs["age"][0])
            return str(today - age)

def say_bye(hour):
    switcher = {
        0: "Good Night!",
        1: "Good Night!",
        2: "Good Night!",
        3: "Good Night!",
        4: "Good Night!",
        5: "Good Night!",
        6: "Good Morning!",
        7: "Good Morning!",
        8: "Good Morning!",
        9: "Good Morning!",
        10: "Good Morning!",
        11: "Good Morning!",
        12: "Good Morning!",
        13: "Good Day!",
        14: "Good Day!",
        15: "Good Day!",
        16: "Good Day!",
        17: "Good Evening!",
        18: "Good Evening!",
        19: "Good Evening!",
        20: "Good Evening!",
        21: "Good Night!",
        22: "Good Night!",
        23: "Good Night!",
        24: "Good Night!"
    }

    return switcher.get(hour, "Invalid time")

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