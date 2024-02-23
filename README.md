# dns_app

## Authenticated DNS Server

To build the Docker image and test the server, you will need to perform the following steps on your local machine where Docker is installed. I will guide you through the process:

1. **Prepare your files**: Ensure that the refactored `as.py` script and the `Dockerfile` are in the same directory on your local system.

2. **Build the Docker image**: Open a terminal and navigate to the directory containing your files. Run the following command to build the Docker image:

```bash
docker build -t as-server .
```

This command builds an image and tags it as `as-server`. The period at the end of the command signifies that Docker should look for the `Dockerfile` in the current directory.

3. **Run the Docker container**: Once the image is built, run the container using the image with the following command:

```bash
docker run -dp 53533:53533/udp as-server
```

This command runs the container in detached mode (due to `-d`), maps the port `53533` on the host to `53533` on the container (due to `-p 53533:53533/udp`), and uses the `as-server` image to run the container.

4. **Test the server**:

    - To test the registration, you can send a UDP packet with a tool like `netcat` (nc) from another terminal window:

    ```bash
    echo -n "TYPE=A\nNAME=test.com\nVALUE=1.2.3.4" | nc -u -w1 localhost 53533
    ```

    You should receive "Success" as a response.

    - To test the query, you can send another UDP packet:

    ```bash
    echo -n "TYPE=A\nNAME=test.com" | nc -u -w1 localhost 53533
    ```

    You should receive a response that includes the name and value that you registered.

5. **Check logs**: You can check the logs of your Docker container to see the server's output:

```bash
docker logs [container_id]
```

You can find your container's ID by running `docker ps`.

After you have successfully tested the `as.py` server, we can proceed with the `fs.py` script. Please provide the `fs.py` script you want to refactor, or let me know the requirements for the Fibonacci Server, and I will assist you with that.

## Fibonacci Server
