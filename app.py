from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


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


if __name__ == "__main__":
    app.run(debug=True)
