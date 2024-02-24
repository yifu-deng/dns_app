FROM python:3.8-slim

WORKDIR /usr/src/app

COPY . .
RUN pip install Flask
EXPOSE 53533/udp

CMD ["python", "server.py"]
