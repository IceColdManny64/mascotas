import re

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from app.models.user import User, UserRole

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def loose_email(form, field):
    if not EMAIL_RE.match(field.data or ""):
        raise ValidationError("Ingresa un email válido.")


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), loose_email, Length(max=150)])
    password = PasswordField(
        "Contraseña", validators=[DataRequired(), Length(min=8, max=128)]
    )
    name = StringField("Nombre", validators=[DataRequired(), Length(max=150)])
    role = SelectField(
        "Tipo de cuenta",
        choices=[("adopter", "Adoptante"), ("shelter", "Refugio")],
        validators=[DataRequired()],
    )
    city = StringField("Ciudad", validators=[Length(max=100)])
    submit = SubmitField("Registrarse")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("Este email ya está registrado.")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), loose_email])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar sesión")