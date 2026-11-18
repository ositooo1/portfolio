from werkzeug.security import generate_password_hash, check_password_hash

from extensiones import db


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def establecer_clave(self, clave):
        self.password_hash = generate_password_hash(clave)

    # Encapsulamiento: la comparación contra el hash queda dentro de Usuario.
    # El resto del programa nunca maneja el hash directamente.
    def verificar_clave(self, clave):
        return check_password_hash(self.password_hash, clave)


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
    cv = db.Column(db.String(255))


class RedSocial(db.Model):
    __tablename__ = "red_social"

    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil.id"), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    icono = db.Column(db.String(50))


class Experiencia(db.Model):
    __tablename__ = "experiencia"

    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil.id"), nullable=False)
    empresa = db.Column(db.String(120), nullable=False)
    puesto = db.Column(db.String(120), nullable=False)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    descripcion = db.Column(db.Text)
    orden = db.Column(db.Integer, default=0)


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
