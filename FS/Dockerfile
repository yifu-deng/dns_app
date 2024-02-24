FROM python:3.8-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install Flask
RUN pip install requests

EXPOSE 9090

ENV FLASK_ENV=production

CMD ["flask", "run", "--host=0.0.0.0", "--port=9090"]
