from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import Length, NumberRange, Optional

from app.forms.pets import SIZE_CHOICES, SPECIES_CHOICES


class AlertForm(FlaskForm):
    species = SelectField("Especie", choices=SPECIES_CHOICES, validators=[Optional()])
    breed = StringField("Raza", validators=[Optional(), Length(max=100)])
    age_max = IntegerField(
        "Edad máxima", validators=[Optional(), NumberRange(min=0, max=30)]
    )
    size = SelectField("Tamaño", choices=SIZE_CHOICES, validators=[Optional()])
    children_friendly = BooleanField("Apto con niños")
    other_animals_friendly = BooleanField("Apto con otros animales")
    submit = SubmitField("Crear alerta")
