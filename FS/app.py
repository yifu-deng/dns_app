from flask import Flask, request, Response, abort
import requests
import os

ROUTE_REGISTER = "/register"
ROUTE_FIBONACCI = "/fabonacci"
AS_SERVER_ADDRESS = "http://0.0.0.0:53533"

app = Flask(__name__)


@app.route("/")
def fs_welcome():
    return "Welcome to the FS Web Service. Please use /register to register your hostname."


@app.route(ROUTE_REGISTER)
def register():
    host_name = request.args.get("hostname")
    if not host_name:
        abort(400, description="Missing required parameter: hostname")

    ip_address = os.getenv("IP_ADDRESS", "0.0.0.0")
    host_info = {"name": host_name, "address": ip_address}
    try:
        r = requests.post(AS_SERVER_ADDRESS, json=host_info)
    except requests.exceptions.RequestException as e:
        return str(e)
    return r.text


@app.route(ROUTE_FIBONACCI)
def fabonacci():
    number = request.args.get("number")
    if not number:
        abort(400, description="Missing required parameter: number")

    res = fibonacci(int(number))
    return Response(f"the fibo for {number} is: {res}", status=200)


def fibonacci(n):
    fib_values = [0, 1] + [0] * (n - 1)
    for i in range(2, n + 1):
        fib_values[i] = fib_values[i - 1] + fib_values[i - 2]
    return fib_values[n]


app.run(host="0.0.0.0", port=9090, debug=True)
