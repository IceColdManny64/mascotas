from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class ReviewForm(FlaskForm):
    rating = IntegerField(
        "Valoración (1-5)",
        validators=[DataRequired(), NumberRange(min=1, max=5)],
    )
    comment = TextAreaField("Comentario", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Enviar valoración")


class ReportReviewForm(FlaskForm):
    reason = StringField(
        "Motivo del reporte",
        validators=[DataRequired(), Length(max=200)],
    )
    submit = SubmitField("Reportar")
