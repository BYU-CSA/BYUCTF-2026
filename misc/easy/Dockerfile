FROM python:slim AS app
# RUN pip install --no-cache-dir progress

FROM pwn.red/jail

COPY --from=app / /srv
COPY ./src/jail.py /srv/app/run
COPY ./src/flag.txt /srv/app/
COPY --from=app /usr/bin/bash /srv/app/

ENV JAIL_MEM=20M JAIL_ENV_NUM=5