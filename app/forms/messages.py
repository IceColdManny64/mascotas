from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    content = TextAreaField(
        "Mensaje",
        validators=[DataRequired(), Length(min=1, max=1000)],
    )
    pet_id = HiddenField()
    submit = SubmitField("Enviar")
