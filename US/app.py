from flask import Flask, request, Response, abort
import requests

app = Flask(__name__)


@app.route("/")
def us_welcome():
    return "Welcome to the Fibonacci App!"


@app.route("/fibonacci")
def US():
    required_params = ["hostname", "fs_port", "number", "as_ip", "as_port"]
    for param in required_params:
        if param not in request.args:
            abort(400, description=f"Missing required parameter: {param}")

    host_name = request.args["hostname"]
    fs_port = request.args["fs_port"]
    number = request.args["number"]
    as_ip = request.args["as_ip"]
    as_port = request.args["as_port"]

    print(f"Success, info input: {host_name}, {fs_port}, {number}, {as_ip}, {as_port}")

    # ask address from AS
    ip_info = {"name": host_name, "fs_port": fs_port}
    response = requests.get(f"http://{as_ip}:{as_port}", params=ip_info)

    if response.status_code == 404:
        return "hostname not found, Status:404"

    # send request to FS
    fs_url = f"http://{response.text}:{fs_port}/fabonacci"
    fs_response = requests.get(fs_url, params={"number": number})

    # output result
    return fs_response.text


app.run(host="0.0.0.0", port=8080, debug=True)
