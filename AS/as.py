import logging
from socket import socket, AF_INET, SOCK_DGRAM

# Constants
SERVER_PORT = 53533
BUFFER_SIZE = 2048
SUCCESS_MESSAGE = "Success"
ERROR_NAME_REGISTERED = "Error: Name is already registered"
ERROR_NAME_NOT_FOUND = "Error: Name not found"

# Configure logging
logging.basicConfig(level=logging.INFO)


def handle_registration(data, client_address):
    name, value = data[1].split("=")[1], data[2].split("=")[1]
    if name in mappings:
        logging.warning(f"Attempt to re-register name: {name}")
        return ERROR_NAME_REGISTERED
    else:
        mappings[name] = value
        logging.info(f"Registered name: {name} with value: {value}")
        return SUCCESS_MESSAGE


def handle_query(data):
    name = data[1].split("=")[1]
    if name in mappings:
        value = mappings[name]
        logging.info(f"Query for name: {name} returned value: {value}")
        return f"TYPE=A\nNAME={name}\nVALUE={value}\nTTL=10"
    else:
        logging.warning(f"Query for unregistered name: {name}")
        return ERROR_NAME_NOT_FOUND


# Create a socket (UDP)
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(("", SERVER_PORT))

mappings = {}

logging.info(f"The server is ready to receive messages on port {SERVER_PORT}...")

while True:
    message, client_address = server_socket.recvfrom(BUFFER_SIZE)
    data = message.decode().split("\n")
    logging.info(f"Received message from {client_address}: {data}")

    if "VALUE" in message.decode():  # Handle registration
        response = handle_registration(data, client_address)
    else:  # Handle query
        response = handle_query(data)

    server_socket.sendto(response.encode(), client_address)
