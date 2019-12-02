from flask import Flask, request
import logging
import time
import json

app = Flask(__name__)
MESSAGES = [
    {"username": "John", "time": time.time(), "text": "Hello!"}
]

@app.route("/send")
def send_mesage():
    """
    :param json: {"username":str,"text":str}
    :return: {"ok":bool}
    """
    username = request.json["username"]
    text = request.json["text"]
    if not isinstance(username, str) or len(username) == 0:
        return {"ok": False}
    if not isinstance(text, str) or len(text) == 0:
        return {"ok": False}

    app.logger.info(username)
    app.logger.info(text)

    # TODO ave message
    MESSAGES.append({"username": username, "time": time.time(), "text": text})

    return {"ok": True}


@app.route("/get_messages")
def get_messages():
    """
    :return: {"messages": ["username": str, "time": str, "text": str]}
    """
    return {"messages": MESSAGES}


app.run(debug=True)
