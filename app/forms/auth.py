from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models.user import User, UserRole


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=150)])
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
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar sesión")
