FROM debian:trixie-slim

WORKDIR /app-manager

COPY . /app-manager

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    python3 \
    python3-pip \
    python3-venv \
    ca-certificates \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /app-manager/pvenv \
 && mkdir -p /app-manager/apps \
 && touch /app-manager/config.json


COPY installer/* /app-manager/installer/

COPY start.py /app-manager

COPY config.json /app-manager

RUN chmod +x /app-manager/start.py

CMD ["bash"]
