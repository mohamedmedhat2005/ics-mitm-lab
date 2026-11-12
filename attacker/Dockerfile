FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    iproute2 iputils-ping net-tools tcpdump nmap \
    iptables gcc python3-dev libnetfilter-queue-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir scapy pymodbus netfilterqueue
WORKDIR /app
COPY . /app
CMD ["sleep", "infinity"]
