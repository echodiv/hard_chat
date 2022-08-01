FROM python:3.10-alpine

RUN apk update

WORKDIR /app
COPY ./hardchat_srv .

RUN python -m venv .venv

RUN .venv/bin/pip install --upgrade pip 
RUN .venv/bin/pip install -r requirements.txt
RUN .venv/bin/pip install gunicorn

ENV FLASK_APP /app/hardchat.py

ENTRYPOINT ["/app/boot.sh"]
