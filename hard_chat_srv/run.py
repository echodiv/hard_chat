from app import create_app, db
from app.models import Users, Chats, Messages, Talkers

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 
            'Users': Users,
            'Chats': Chats,
            'Messages': Messages,
            'Talkers': Talkers}
