from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.forms.auth import LoginForm, RegisterForm
from app.models.user import User, UserRole

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        form = RegisterForm()
        return render_template("auth/register.html", form=form)

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data.lower(),
            password_hash=generate_password_hash(form.password.data),
            name=form.name.data,
            role=UserRole(form.role.data),
            city=form.city.data or None,
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("¡Registro exitoso! Bienvenido.", "success")
        return redirect(url_for("pets.index"))
    return render_template("auth/register.html", form=form), 200


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        form = LoginForm()
        return render_template("auth/login.html", form=form)

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None or not check_password_hash(user.password_hash, form.password.data):
            flash("Credenciales inválidas", "danger")
            return render_template("auth/login.html", form=form), 200
        if user.is_suspended:
            flash("Cuenta suspendida", "danger")
            return render_template("auth/login.html", form=form), 200
        login_user(user)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("pets.index"))
    return render_template("auth/login.html", form=form), 200


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
