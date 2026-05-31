FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    curl \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libasound2t64 \
    libxshmfence1 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Create ctf user and directory
RUN mkdir /ctf
WORKDIR /ctf
RUN useradd -M -d /ctf ctf

# Install Python and Node dependencies
RUN pip3 install flask
RUN npm install --force puppeteer

# Copy files
COPY app.py /ctf/app.py
COPY admin_bot.js /ctf/admin_bot.js
COPY start.sh /ctf/start.sh

# Set permissions
RUN chown -R root:ctf /ctf && \
    chmod -R 750 /ctf && \
    chmod +x /ctf/start.sh

EXPOSE 5000

CMD ["bash", "/ctf/start.sh"]
