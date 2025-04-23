FROM debian:bookworm-slim

WORKDIR /app-manager

COPY . /app-manager

RUN apt-get update && apt-get install -y --no-install-recommends \
	bash \
	python3 \
	python3-pip \
	python3-venv \
	ca-certificates \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

RUN chmod +x /app-manager/start.py

RUN mkdir /app-manager/pvenv && \
	mkdir /app-manager/apps &&

RUN touch /app-manager/config.json

COPY installer/* /app-manager/installer/

COPY start.py /app-manager

COPY config.json /app-manager

CMD ["bash"]

ENTRYPOINT ["/app-manager/start.py"]
