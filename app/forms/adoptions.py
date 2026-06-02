from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class AdoptionForm(FlaskForm):
    home_type = SelectField(
        "Tipo de vivienda",
        choices=[
            ("house", "Casa"),
            ("apartment", "Apartamento"),
            ("farm", "Finca"),
        ],
        validators=[DataRequired()],
    )
    has_yard = BooleanField("Tiene patio")
    other_pets = BooleanField("Tiene otras mascotas")
    other_pets_desc = StringField(
        "Descripción otras mascotas", validators=[Optional(), Length(max=200)]
    )
    has_children = BooleanField("Tiene hijos")
    children_ages = StringField(
        "Edades de los hijos", validators=[Optional(), Length(max=100)]
    )
    experience = TextAreaField(
        "Experiencia con mascotas",
        validators=[DataRequired(), Length(min=50)],
    )
    motivation = TextAreaField(
        "Motivación para adoptar",
        validators=[DataRequired(), Length(min=50)],
    )
    submit = SubmitField("Enviar solicitud")
