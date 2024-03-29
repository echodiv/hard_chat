from app import create_app, db
from app.models import Messages, Notifications, Posts, Users

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Users": Users,
        "Posts": Posts,
        "Messages": Messages,
        "Notification": Notifications,
    }
