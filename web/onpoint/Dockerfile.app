FROM python:3.11-slim

RUN mkdir /ctf
WORKDIR /ctf

RUN useradd -M -d /ctf ctf

RUN pip3 install flask

COPY app.py /ctf/app.py
COPY secret_key.txt /ctf/secret_key.txt
COPY templates/ /ctf/templates/

RUN chown -R root:ctf /ctf && chmod -R 750 /ctf

EXPOSE 5000
CMD ["python3", "/ctf/app.py"]
