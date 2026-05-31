FROM python:3.12-slim AS app

# dependencies
RUN apt-get update
RUN apt-get upgrade -y
RUN rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy challenge files
FROM pwn.red/jail
COPY --from=app / /srv

WORKDIR /srv/app

COPY flag.txt .
COPY utils.py .
COPY chall.py run

# Setup the environment
ENV JAIL_TIME=60 JAIL_MEM=20M JAIL_CONNS_PER_IP=10
