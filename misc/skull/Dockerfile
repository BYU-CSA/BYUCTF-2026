FROM ubuntu:latest

# dependencies
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y socat
RUN rm -rf /var/lib/apt/lists/*

# setup unpriv user
RUN mkdir -p /ctf/19ecae731566ee058943b0ac569ea9ef
RUN mkdir -p /ctf/7169d2872cdac0f85b135c02bc20c1a3
RUN useradd -M -d /ctf ctf

# copy files
RUN echo "Connection blocked" > /etc/banner_fail
COPY ctf.xinetd /etc/xinetd.d/ctf
COPY src/jail.sh /ctf/19ecae731566ee058943b0ac569ea9ef/
COPY src/flag /ctf/19ecae731566ee058943b0ac569ea9ef/solution

# file perms
RUN chown -R root:ctf /ctf/
RUN chmod -R 750 /ctf/

RUN mv /usr/bin/*sh /ctf/7169d2872cdac0f85b135c02bc20c1a3

# run
CMD ["socat", "-T60", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:/ctf/19ecae731566ee058943b0ac569ea9ef/jail.sh,pty,stderr,echo=0"]
EXPOSE 5000