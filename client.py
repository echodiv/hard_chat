import requests


def get_messagess():
    res = requests.get("http://127.0.0.1:5000/get_messages")
    if res.status_code == 200:
        print(res.text)
        print(res.json())


def send_message(username, msg):
    if not isinstance(username, str) and len(username) == 0:
        raise Exception("invalid username")
    if not isinstance(msg, str) and len(msg) == 0:
        raise Exception("invalid message")
    req = requests.post(
        "http://127.0.0.1:5000/send",
        json={'username': 'username', 'text': 'msg'}
    )
    # if req.status_code == 200:
    #     print
    print(req.status_code, "\n", req.json())


if __name__ == "__main__":
    send_message("Ilyas", "azazaza")