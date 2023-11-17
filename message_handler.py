import json
import logging
import socket
import urllib.parse
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("messages")
logger.addHandler(logging.StreamHandler())


def run_tcp_server():
    host = socket.gethostbyname(socket.gethostname())
    port = 5000
    server_socket = socket.socket()

    server_socket.bind((host, port))
    server_socket.listen(5)
    logger.info("socket server started!")
    try:
        while True:
            conn, addr = server_socket.accept()

            print(conn)
            while True:
                data = conn.recv(1024)

                if not data:
                    break

            conn.close()
    except KeyboardInterrupt:
        logger.info("Shutting down tcp server...")
    finally:
        server_socket.close()


def save_message(message):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = urllib.parse.unquote_plus(message)

    message = {
        key: value for key, value in [el.split("=") for el in message.split("&")]
    }

    with open("storage/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data.update({time: message})
    with open("storage/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f)
