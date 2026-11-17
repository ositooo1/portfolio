import os
from functools import wraps

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    request,
    abort,
    send_from_directory,
)

import config
from errores import ErrorDeValidacion
from extensiones import db, csrf
from forms import LoginForm
from gestores import GESTORES
from modelos import (
    Usuario,
    Perfil,
    RedSocial,
    Experiencia,
    Educacion,
    Habilidad,
    Proyecto,
)
from subidas import SubidaFoto, SubidaBanner, SubidaCV

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CARPETA_IMG = os.path.join(BASE_DIR, "static", "img")
CARPETA_DOCS = os.path.join(BASE_DIR, "static", "docs")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024

db.init_app(app)
csrf.init_app(app)

SUBIDAS = {
    "foto": SubidaFoto(CARPETA_IMG),
    "banner": SubidaBanner(CARPETA_IMG),
    "cv": SubidaCV(CARPETA_DOCS),
}


def login_requerido(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return vista(*args, **kwargs)

    return envoltura


@app.context_processor
def inyectar_estado():
    return {"editando": "usuario_id" in session}


@app.errorhandler(413)
def archivo_muy_grande(error):
    flash("El archivo es demasiado grande.")
    return redirect(url_for("inicio"))


@app.route("/")
def inicio():
    perfil = Perfil.query.first()
    redes = RedSocial.query.filter_by(perfil_id=perfil.id).all()
    experiencias = (
        Experiencia.query.filter_by(perfil_id=perfil.id)
        .order_by(Experiencia.orden, Experiencia.fecha_inicio.desc())
        .all()
    )
    estudios = (
        Educacion.query.filter_by(perfil_id=perfil.id)
        .order_by(Educacion.orden, Educacion.fecha_inicio.desc())
        .all()
    )
    habilidades = (
        Habilidad.query.filter_by(perfil_id=perfil.id)
        .order_by(Habilidad.orden, Habilidad.id)
        .all()
    )
    proyectos = (
        Proyecto.query.filter_by(perfil_id=perfil.id)
        .order_by(Proyecto.orden, Proyecto.id)
        .all()
    )
    return render_template(
        "index.html",
        perfil=perfil,
        redes=redes,
        experiencias=experiencias,
        estudios=estudios,
        habilidades=habilidades,
        proyectos=proyectos,
    )


@app.route("/cv")
def descargar_cv():
    perfil = Perfil.query.first()
    if not perfil.cv:
        abort(404)
    return send_from_directory(
        CARPETA_DOCS,
        perfil.cv,
        as_attachment=True,
        download_name=f"CV - {perfil.nombre}.pdf",
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    perfil = Perfil.query.first()
    redes = RedSocial.query.filter_by(perfil_id=perfil.id).all()
    form = LoginForm()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        if usuario and usuario.verificar_clave(form.password.data):
            session.clear()
            session["usuario_id"] = usuario.id
            return redirect(url_for("inicio"))
        flash("Usuario o contraseña incorrectos.")

    return render_template("login.html", perfil=perfil, redes=redes, form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))


@app.route("/guardar/<seccion>", methods=["POST"])
@login_requerido
def guardar(seccion):
    gestor = GESTORES.get(seccion)
    if gestor is None:
        abort(404)

    try:
        gestor.guardar(request.form)
        flash("Cambios guardados.")
    except ErrorDeValidacion as error:
        flash(str(error))
    return redirect(url_for("inicio") + "#" + gestor.ancla())


@app.route("/eliminar/<seccion>/<int:id>", methods=["POST"])
@login_requerido
def eliminar(seccion, id):
    gestor = GESTORES.get(seccion)
    if gestor is None:
        abort(404)

    try:
        gestor.eliminar(id)
        flash("Elemento eliminado.")
    except ErrorDeValidacion as error:
        flash(str(error))
    return redirect(url_for("inicio") + "#" + gestor.ancla())


@app.route("/subir/<tipo>", methods=["POST"])
@login_requerido
def subir(tipo):
    subida = SUBIDAS.get(tipo)
    if subida is None:
        abort(404)

    try:
        subida.reemplazar(request.files.get("archivo"))
        flash("Archivo actualizado.")
    except ErrorDeValidacion as error:
        flash(str(error))
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
