import socket

# Details for the AS
as_address = "127.0.0.1"
as_port = 53533

# Simulated DNS query request
dns_query_request = "TYPE=A\nNAME=fibonacci.com"

# Setup UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send DNS query request
sock.sendto(dns_query_request.encode(), (as_address, as_port))

# Receive and print the response
response, _ = sock.recvfrom(1024)
print("DNS Query response:", response.decode())

sock.close()
