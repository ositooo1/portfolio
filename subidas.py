import os
import secrets
from abc import ABC, abstractmethod

from extensiones import db
from errores import ErrorDeValidacion
from modelos import Perfil

MB = 1024 * 1024


# Abstracción: define el proceso de subir un archivo (validar y reemplazar).
# Cada tipo de subida indica su campo, sus formatos y su tamaño máximo.
class Subida(ABC):
    def __init__(self, carpeta):
        # Encapsulamiento: la carpeta y la detección de formato son privadas.
        # Solo se usan desde dentro de la clase.
        self.__carpeta = carpeta

    @property
    def carpeta(self):
        return self.__carpeta

    @abstractmethod
    def campo(self): ...

    @abstractmethod
    def formatos(self): ...

    @abstractmethod
    def maximo(self): ...

    def __detectar_formato(self, cabecera):
        if cabecera.startswith(b"\xff\xd8\xff"):
            return "jpg"
        if cabecera.startswith(b"\x89PNG\r\n\x1a\n"):
            return "png"
        if cabecera[:4] == b"RIFF" and cabecera[8:12] == b"WEBP":
            return "webp"
        if cabecera.startswith(b"%PDF"):
            return "pdf"
        return None

    def __borrar(self, nombre):
        if nombre:
            ruta = os.path.join(self.carpeta, os.path.basename(nombre))
            if os.path.isfile(ruta):
                os.remove(ruta)

    def validar(self, archivo):
        if not archivo or not archivo.filename:
            raise ErrorDeValidacion("Elegí un archivo para subir.")

        formato = self.__detectar_formato(archivo.stream.read(16))
        archivo.stream.seek(0, os.SEEK_END)
        tamano = archivo.stream.tell()
        archivo.stream.seek(0)

        if formato not in self.formatos():
            raise ErrorDeValidacion(
                "Formato no permitido: "
                + ", ".join(sorted(self.formatos())).upper()
                + "."
            )
        if tamano > self.maximo():
            raise ErrorDeValidacion(
                f"El archivo supera el máximo de {self.maximo() // MB} MB."
            )
        return formato

    def reemplazar(self, archivo):
        formato = self.validar(archivo)

        nombre = f"{self.campo()}-{secrets.token_hex(8)}.{formato}"
        os.makedirs(self.carpeta, exist_ok=True)
        archivo.save(os.path.join(self.carpeta, nombre))

        perfil = Perfil.query.first()
        anterior = getattr(perfil, self.campo())
        setattr(perfil, self.campo(), nombre)
        db.session.commit()

        self.__borrar(anterior)


class SubidaImagen(Subida):
    def formatos(self):
        return {"jpg", "png", "webp"}


# Herencia: SubidaFoto hereda de SubidaImagen, que a su vez hereda de Subida.
# Toma los formatos de imagen y solo define su campo y su tamaño máximo.
class SubidaFoto(SubidaImagen):
    def campo(self):
        return "foto"

    def maximo(self):
        return 3 * MB


class SubidaBanner(SubidaImagen):
    def campo(self):
        return "banner"

    def maximo(self):
        return 5 * MB


class SubidaCV(Subida):
    def campo(self):
        return "cv"

    def formatos(self):
        return {"pdf"}

    def maximo(self):
        return 5 * MB
