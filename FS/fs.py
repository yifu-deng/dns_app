from flask import Flask, request, jsonify
from socket import socket, AF_INET, SOCK_DGRAM
import json

app = Flask(__name__)
AS_UDP_IP = "10.9.10.2"
AS_UDP_PORT = 53533
FS_NAME = "fibonacci.com"
FS_IP = "172.18.0.2"


def register_with_as(hostname, ip, as_ip, as_port):
    with socket(AF_INET, SOCK_DGRAM) as sock:
        message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
        sock.sendto(message.encode(), (as_ip, int(as_port)))


def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@app.route("/register", methods=["PUT"])
def register():
    data = request.get_json()
    register_with_as(data["hostname"], data["ip"], data["as_ip"], data["as_port"])
    return "", 201


@app.route("/fibonacci")
def get_fibonacci():
    number = request.args.get("number", default=1, type=int)
    if not isinstance(number, int) or number < 0:
        return "Bad Format", 400
    return jsonify(fibonacci_number=fibonacci(number)), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
