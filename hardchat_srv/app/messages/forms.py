from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    """Send message to another user"""

    LABELS = {
        "message": _l("Message"),
        "button": _l("Submit"),
    }

    message = TextAreaField(
        LABELS["message"], validators=[DataRequired(), Length(min=0, max=140)]
    )
    submit = SubmitField(LABELS["button"])
