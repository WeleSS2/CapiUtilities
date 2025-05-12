FROM debian:trixie-slim

WORKDIR /app-manager

COPY . /app-manager

ARG PROFILE=default

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    python3 \
    python3-pip \
    python3-venv \
    ca-certificates \
    libgl1 \
    libegl1 \
    libxkbcommon-x11-0 \
    libxcb1 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-shm0 \
    libxcb-cursor0 \
    libxcb-xinerama0 \
    libxcb-icccm4 \
    libxcb-keysyms1 \
    libxcomposite1 \
    libxcursor1 \
    libxrandr2 \
    libxdamage1 \
    libxfixes3 \
    libfontconfig1 \
    libglib2.0-0 \
    libdbus-1-3 \
 && apt-get clean && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /app-manager/pvenv \
 && mkdir -p /app-manager/apps \
 && touch /app-manager/config.json


 
COPY installer/* /app-manager/installer/

COPY start.py /app-manager

COPY config.json /app-manager

ENV VENV_PATH=/app-manager/pvenv
RUN python3 -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

RUN pip install --upgrade pip \
    && if [ -f installer/${PROFILE}.txt ]; then \
         pip install --no-cache-dir -r installer/${PROFILE}.txt; \
       fi

EXPOSE 8000

CMD ["bash"]
