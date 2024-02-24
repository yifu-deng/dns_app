# DNS Application System

## Overview

This project implements a simplified DNS system with three main components:

- **User Server (US):** A Flask-based HTTP server that processes requests for Fibonacci numbers, requiring DNS resolution to communicate with the Fibonacci Server (FS).
- **Fibonacci Server (FS):** A Flask-based HTTP server that calculates Fibonacci numbers and registers itself with the Authoritative Server (AS) for DNS resolution.
- **Authoritative Server (AS):** Manages DNS records, handling registration requests and responding to DNS queries.

## Operational Flow

The DNS Application System operates through a sequence of steps that demonstrate the interaction between the User Server (US), Fibonacci Server (FS), and Authoritative Server (AS):

1. **Fibonacci Server Registration:** The FS registers its hostname and IP address with the AS. This registration is necessary for the AS to recognize and resolve requests for the FS.

2. **DNS Record Creation:** Upon registration, the AS creates a DNS record for the FS, enabling it to respond to DNS queries with the FS's IP address.

3. **Registration Acknowledgment:** The AS sends a response back to the FS indicating the success or failure of the registration process.

4. **User Request Initiation:** A user initiates a request to calculate a Fibonacci number by visiting a URL structured as follows:

   ```
   http://<P_HTTP_SERVER>:<PORT>/fibonacci?hostname=fibonacci.com&fs_port=9090&number=10&as_ip=3.4.5.6&as_port=53533
   ```

   This request includes the hostname of the FS, the port number of the FS, the Fibonacci number to calculate, and the IP address and port number of the AS.

5. **DNS Query:** The US parses the hostname from the query and sends a DNS query to the AS to resolve the FS's IP address.

6. **DNS Query Response:** The AS responds to the DNS query with the IP address of the FS, enabling the US to direct the Fibonacci calculation request to the correct server.

7. **Fibonacci Calculation Request:** The US sends a request to the FS using the resolved IP address:

   ```
   http://<FIBONACCI_SERVER_IP>/fibonacci?number=8
   ```

8. **Fibonacci Calculation and Response:** The FS calculates the requested Fibonacci number and returns the result to the US with an HTTP 200 status code.

9. **Result Delivery to User:** The US then relays the Fibonacci calculation result back to the user.

## Getting Started

### Prerequisites

- Docker
- Python 3.8 or later
- Flask
- Requests library for Python

### Installation

1. Clone the repository to your local machine.
2. Navigate to each server's directory (`US`, `FS`, `AS`) and build their Docker images using the provided Dockerfiles.

   ```sh
   docker build -t <your_image_name>:latest .
   ```

3. Create a Docker network to facilitate communication between containers:

   ```sh
   docker network create dns_network
   ```

4. Run the containers specifying the network name:

   ```sh
   docker run --network dns_network --name <container_name> -p <external_port>:<internal_port> -d <your_image_name>:latest
   ```

### Configuration

- Each server can be configured through its respective source code or Dockerfile, depending on the environment variables or settings you wish to adjust.

## Usage

### User Server (US)

- Start the US and make a GET request to `/fibonacci` with the required parameters (`hostname`, `fs_port`, `number`, `as_ip`, `as_port`).
- If any parameter is missing, the server will return an HTTP 400 error code.

### Fibonacci Server (FS)

- FS accepts a PUT request at `/register` for initial setup and registration with the AS.
- It also serves the `/fibonacci` path for calculating Fibonacci numbers given a sequence number `X`.

### Authoritative Server (AS)

- Handles UDP connections on port 53533 for DNS record registration.
- Responds to DNS queries with the registered IP address and other details.

## Deployment on IBM Cloud Kubernetes Service

- Refer to `deploy_dns.yml` for a Kubernetes deployment example.
- Use `kubectl apply -f deploy_dns.yml` to deploy the application to your IBM Cloud Kubernetes cluster.
