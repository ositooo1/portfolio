from getpass import getpass

from werkzeug.security import generate_password_hash

from app import app, db, Usuario

with app.app_context():
    if Usuario.query.count() > 0:
        print("Ya existe un usuario. Este portfolio admite uno solo.")
    else:
        username = input("Usuario: ").strip()
        clave = getpass("Contraseña: ")
        repetir = getpass("Repetir contraseña: ")

        if not username or len(clave) < 8:
            print(
                "El usuario no puede estar vacío y la contraseña debe tener al menos 8 caracteres."
            )
        elif clave != repetir:
            print("Las contraseñas no coinciden.")
        else:
            db.session.add(
                Usuario(username=username, password_hash=generate_password_hash(clave))
            )
            db.session.commit()
            print("Usuario creado.")
