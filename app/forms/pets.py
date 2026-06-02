from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, MultipleFileField
from wtforms import (
    BooleanField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional

SPECIES_CHOICES = [
    ("", "Todas"),
    ("dog", "Perro"),
    ("cat", "Gato"),
    ("rabbit", "Conejo"),
    ("bird", "Ave"),
    ("other", "Otro"),
]

SIZE_CHOICES = [
    ("", "Todos"),
    ("small", "Pequeño"),
    ("medium", "Mediano"),
    ("large", "Grande"),
]


class PetForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    species = SelectField(
        "Especie",
        choices=[c for c in SPECIES_CHOICES if c[0]],
        validators=[DataRequired()],
    )
    breed = StringField("Raza", validators=[Optional(), Length(max=100)])
    age_years = IntegerField(
        "Edad (años)", validators=[Optional(), NumberRange(min=0, max=30)]
    )
    size = SelectField("Tamaño", choices=SIZE_CHOICES, validators=[Optional()])
    temperament = StringField("Temperamento", validators=[Optional(), Length(max=200)])
    description = TextAreaField("Descripción", validators=[DataRequired()])
    medical_history = TextAreaField("Historial médico", validators=[Optional()])
    special_requirements = TextAreaField("Requisitos especiales", validators=[Optional()])
    children_friendly = BooleanField("Apto con niños")
    other_animals_friendly = BooleanField("Apto con otros animales")
    photos = MultipleFileField("Fotos")
    submit = SubmitField("Guardar")


class PetCreateForm(PetForm):
    photos = MultipleFileField(
        "Fotos (mínimo 1, máximo 5)",
        validators=[FileRequired(message="Debes subir al menos una foto.")],
    )


class SearchForm(FlaskForm):
    species = SelectField("Especie", choices=SPECIES_CHOICES, validators=[Optional()])
    breed = StringField("Raza", validators=[Optional(), Length(max=100)])
    age_min = IntegerField("Edad mín.", validators=[Optional(), NumberRange(min=0, max=30)])
    age_max = IntegerField("Edad máx.", validators=[Optional(), NumberRange(min=0, max=30)])
    size = SelectField("Tamaño", choices=SIZE_CHOICES, validators=[Optional()])
    location = StringField("Ubicación", validators=[Optional(), Length(max=100)])
    children_friendly = BooleanField("Apto con niños")
    other_animals_friendly = BooleanField("Apto con otros animales")
    submit = SubmitField("Buscar")
