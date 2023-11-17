import mimetypes
import pathlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from message_handler import run_tcp_server, save_message


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(
            "GET request received from: "
            + self.client_address[0]
            + ":"
            + str(self.client_address[1])
        )
        if self.path == "/":
            self.load_homepage()
        elif self.path in "/message":
            self.load_message_page()
        else:
            if pathlib.Path(self.path[1:]).exists():
                self.load_static_file()
            else:
                self.load_error_page()

    def do_POST(self):
        print("POST request received")
        data = self.rfile.read(int(self.headers["Content-Length"]))
        print(f"data decoded from POST:{data.decode('utf-8')}")
        save_message(data.decode("utf-8"))
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def load_page(self, file, status=200):
        with open(file, "rb") as f:
            content = f.read()

        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content)

    def load_static_file(self):
        self.send_response(200)
        file = self.path[1:]
        mt = mimetypes.guess_type(self.path[1:])

        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")

        self.end_headers()
        with open(file, "rb") as f:
            self.wfile.write(f.read())

    def load_homepage(self):
        self.load_page("index.html")

    def load_message_page(self):
        self.load_page("message.html")

    def load_error_page(self):
        self.load_page("error.html", 404)


def run_http_server():
    print("starting http server...")
    server_address = ("", 3000)
    httpd = HTTPServer(server_address, Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down server...")
        httpd.server_close()


if __name__ == "__main__":
    tcp_run = Thread(target=run_tcp_server, daemon=True)
    tcp_run.start()
    run_http_server()
