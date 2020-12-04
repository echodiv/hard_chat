FROM python:3.6-alpine

RUN apk update
RUN apk add git

ARG branch
RUN git clone -b ${branch} https://github.com/echodiv/hard_chat.git

RUN adduser -D hardchat

WORKDIR /hard_chat/hardchat_srv
RUN python -m venv .venv
RUN pwd
RUN .venv/bin/pip install --upgrade pip
RUN .venv/bin/pip install -r requirements.txt
RUN .venv/bin/pip install gunicorn

ENV FLASK_APP hardchat.py

RUN chown -R hardchat:hardchat ./
USER hardchat

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
