from flask import Flask, request, jsonify
import socket
import logging
import requests

app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)


@app.route("/fibonacci", methods=["GET"])
def fibonacci():
    hostname = request.args.get("hostname")
    fs_port = request.args.get("fs_port")
    number = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")

    # Validate all parameters are provided
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify("Required parameters are not given"), 400

    logging.info(
        f"Request received: hostname={hostname}, fs_port={fs_port}, number={number}, as_ip={as_ip}, as_port={as_port}"
    )

    # Query the AS for the IP address of the FS
    fs_ip = query_dns(hostname, as_ip, as_port)
    if fs_ip is None:
        return jsonify("Could not find the IP address for the hostname provided"), 500

    # Query the FS for the Fibonacci number
    fib_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
    r = requests.get(fib_url)

    if r.status_code == 200:
        return jsonify(r.json()), 200
    else:
        return jsonify("Error contacting the Fibonacci service"), r.status_code


def query_dns(hostname, as_ip, as_port):
    try:
        # Construct a DNS query message
        msg = f"TYPE=A\nNAME={hostname}\n"
        # Send the message to the AS
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(msg.encode(), (as_ip, int(as_port)))
        # Wait for the response from the AS
        response, _ = client_socket.recvfrom(2048)
        client_socket.close()

        # Parse the response
        response_decoded = response.decode()
        logging.info(f"Response from AS: {response_decoded}")
        if "VALUE=" in response_decoded:
            fs_ip = response_decoded.split("VALUE=")[1].strip()
            return fs_ip
        else:
            return None
    except Exception as e:
        logging.error(f"DNS query failed: {e}")
        return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
