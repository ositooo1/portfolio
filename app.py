from functools import wraps

from flask import Flask, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

import config
from forms import LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

db = SQLAlchemy(app)


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)


class Perfil(db.Model):
    __tablename__ = "perfil"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    email = db.Column(db.String(120))
    ubicacion = db.Column(db.String(100))
    foto = db.Column(db.String(255))
    banner = db.Column(db.String(255))


class RedSocial(db.Model):
    __tablename__ = "red_social"

    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil.id"), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    icono = db.Column(db.String(50))


class Educacion(db.Model):
    __tablename__ = "educacion"

    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil.id"), nullable=False)
    instituto = db.Column(db.String(120), nullable=False)
    carrera = db.Column(db.String(120), nullable=False)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    orden = db.Column(db.Integer, default=0)


class Habilidad(db.Model):
    __tablename__ = "habilidad"

    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil.id"), nullable=False)
    tipo_id = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(60), nullable=False)
    porcentaje = db.Column(db.Integer, nullable=False)
    orden = db.Column(db.Integer, default=0)


class Proyecto(db.Model):
    __tablename__ = "proyecto"

    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil.id"), nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    fecha = db.Column(db.Date)
    descripcion = db.Column(db.Text)
    link = db.Column(db.String(255))
    orden = db.Column(db.Integer, default=0)


def login_requerido(vista):
    """Decorador: protege una ruta. Sin sesión iniciada, manda al login."""

    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return vista(*args, **kwargs)

    return envoltura


@app.route("/")
def inicio():
    perfil = Perfil.query.first()
    redes = RedSocial.query.filter_by(perfil_id=perfil.id).all()
    estudios = (
        Educacion.query.filter_by(perfil_id=perfil.id)
        .order_by(Educacion.orden, Educacion.fecha_inicio.desc())
        .all()
    )
    habilidades = (
        Habilidad.query.filter_by(perfil_id=perfil.id).order_by(Habilidad.orden).all()
    )
    proyectos = (
        Proyecto.query.filter_by(perfil_id=perfil.id).order_by(Proyecto.orden).all()
    )
    return render_template(
        "index.html",
        perfil=perfil,
        redes=redes,
        estudios=estudios,
        habilidades=habilidades,
        proyectos=proyectos,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    perfil = Perfil.query.first()
    redes = RedSocial.query.filter_by(perfil_id=perfil.id).all()
    form = LoginForm()

    # validate_on_submit: es POST, los campos son válidos y el token CSRF coincide
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        if usuario and check_password_hash(usuario.password_hash, form.password.data):
            session.clear()
            session["usuario_id"] = usuario.id
            return redirect(url_for("inicio"))
        # Mensaje genérico: no revela si falló el usuario o la contraseña
        flash("Usuario o contraseña incorrectos.")

    return render_template("login.html", perfil=perfil, redes=redes, form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
