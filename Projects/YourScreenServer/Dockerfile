FROM python:3.13-rc-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    wget \
    unzip \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# Install Python packages
RUN pip install fastapi uvicorn

# Install ngrok
RUN wget -O /tmp/ngrok.zip https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip && \
    unzip /tmp/ngrok.zip -d /usr/local/bin && \
    rm /tmp/ngrok.zip

# Set your ngrok authentication token (Replace below with your token)
ENV NGROK_AUTHTOKEN="2yNuyMuyNdCQUYfEojnE9lfdLlv_5Xi7gjBm3kAFVVoH1Szzo"

# Set working directory
WORKDIR /app

# Copy your app and Nginx config
COPY main.py /app/
COPY nginx.conf /etc/nginx/nginx.conf

# Create required directories
RUN mkdir -p /var/log/nginx /var/run/nginx

# Configure supervisord to run uvicorn, nginx, and ngrok
RUN echo "[supervisord]" > /etc/supervisord.conf && \
    echo "nodaemon=true" >> /etc/supervisord.conf && \
    echo "[program:uvicorn]" >> /etc/supervisord.conf && \
    echo "command=python -m uvicorn main:app --host 127.0.0.1 --port 8000" >> /etc/supervisord.conf && \
    echo "[program:nginx]" >> /etc/supervisord.conf && \
    echo "command=nginx -g 'daemon off;'" >> /etc/supervisord.conf && \
    echo "[program:ngrok]" >> /etc/supervisord.conf && \
    echo "command=ngrok http 80 --log=stdout --authtoken=$NGROK_AUTHTOKEN" >> /etc/supervisord.conf

# Expose ports
EXPOSE 80

# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
