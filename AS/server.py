from flask import Flask, request, Response
import json
import os

app = Flask(__name__)


class AddressService:

    def __init__(self, file_path="address_map.json"):
        self.file_path = file_path
        self.address_map = self.load_address_map()

    def load_address_map(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        else:
            with open(self.file_path, "w") as file:
                json.dump({}, file)
            return {}

    def save_address_map(self):
        with open(self.file_path, "w") as file:
            json.dump(self.address_map, file)

    def get_address(self, name):
        return self.address_map.get(name)

    def set_address(self, name, address):
        self.address_map[name] = address
        self.save_address_map()


address_service = AddressService()


@app.route("/home")
def as_welcome():
    return "Welcome to Authoritative Server home page."


@app.route("/", methods=["GET", "POST"])
def handle_request():
    if request.method == "GET":
        key = request.args.get("name")
        address = address_service.get_address(key)
        if address is None:
            return Response("Hostname not found.", status=404)
        else:
            return Response(address, status=200)
    else:
        data_get = request.form
        host_name = data_get.get("name")
        ip_address = data_get.get("address")

        address_service.set_address(host_name, ip_address)

        return Response("Successfully registered.", status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=53533, debug=True)
