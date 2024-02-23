FROM python:3.10-slim

RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN groupadd -g 799 nyu && \
    useradd -r -u 999 -g nyu nyu

WORKDIR /app

USER nyu

COPY --chown=nyu:nyu . .

EXPOSE 53533

CMD [ "python", "./as.py" ]