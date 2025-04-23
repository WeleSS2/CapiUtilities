FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
	bash \
	python3 \
	python3-pip \
	python3-venv \
	ca-certificates \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

CMD ["bash"]
