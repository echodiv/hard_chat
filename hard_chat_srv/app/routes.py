from flask import render_template
from app import app


@app.route("/")
@app.route("/index")
def index():
    user = {'username': 'Miguel'}
    posts = [{'author': {'username': 'John'},'body': 'Beautiful day in Portland!'},{'author': {'username': 'Susan'},'body': 'The Avengers movie was so cool!'}] 
    return render_template('index.html', title='Home', user=user, posts=posts)


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

