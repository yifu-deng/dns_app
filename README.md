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
- Kubernetes cluster
- `kubectl` command-line tool installed and configured

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

- Edit the `deploy_dns.yml` file in the `kubernetes` directory.
- Use `kubectl apply -f deploy_dns.yml` to deploy the application to the IBM Cloud Kubernetes cluster.
- Apply the `deploy_dns.yml` file to the cluster:

   ```sh
   $kubectl apply -f deploy_dns.yml
   deployment.apps/as-deployment created
   service/as-service created
   deployment.apps/fs-deployment created
   service/fs-service created
   deployment.apps/us-deployment created
   service/us-service created
   ```

- Check the status of your deployments:

   ```sh
   $kubectl get deployments
   NAME            READY   UP-TO-DATE   AVAILABLE   AGE
   as-deployment   1/1     1            1           7m39s
   fs-deployment   1/1     1            1           7m39s
   us-deployment   1/1     1            1           7m39s
   
   $kubectl get pods
   NAME                             READY   STATUS    RESTARTS   AGE
   as-deployment-c768d585c-947l2    1/1     Running   0          8m22s
   fs-deployment-6cf5878ffc-rsxg2   1/1     Running   0          8m22s
   us-deployment-5bc4f95bcb-tl2nc   1/1     Running   0          8m22s
   ```

   And Ensure that all the pods are in a `RUNNING` state.

- Once everything is deployed, you can access the services through the `nodePort` defined in the service configurations. Use the external IP of your Kubernetes cluster nodes with the respective `nodePort` to access each service:
  - Authoritative Server (AS): `http://<node-ip>:30001`
  - Fibonacci Server (FS): `http://<node-ip>:30002`
  - User Server (US): `http://<node-ip>:30003`
  - Replace `<node-ip>` with the actual external IP address of your Kubernetes node.

### Clean Up

- To delete the deployed resources, use the following commands:

   ```sh
   kubectl delete -f kubernetes/deploy_dns.yml
   ```

   This will delete the deployments and services from your Kubernetes cluster.
