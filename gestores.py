from abc import ABC, abstractmethod
from datetime import date

from extensiones import db
from errores import ErrorDeValidacion
from modelos import Perfil, Experiencia, Educacion, Habilidad, Proyecto


class GestorSeccion(ABC):
    def __init__(self):
        self.__campos = self.definir_campos()

    @property
    def campos(self):
        return self.__campos

    @abstractmethod
    def modelo(self): ...

    @abstractmethod
    def definir_campos(self): ...

    @abstractmethod
    def ancla(self): ...

    def __convertir(self, tipo, valor):
        valor = (valor or "").strip()
        try:
            if tipo == "texto":
                return valor or None
            if tipo == "fecha":
                return date.fromisoformat(valor) if valor else None
            return int(valor)
        except ValueError:
            raise ErrorDeValidacion("Valor inválido.")

    def leer(self, formulario):
        datos = {}
        for campo, (tipo, obligatorio) in self.campos.items():
            valor = self.__convertir(tipo, formulario.get(campo))
            if obligatorio and valor is None:
                raise ErrorDeValidacion(f"Falta completar: {campo}.")
            datos[campo] = valor
        self.validar(datos)
        return datos

    def validar(self, datos):
        pass

    def obtener(self, id_elemento):
        if id_elemento:
            return db.get_or_404(self.modelo(), id_elemento)
        return self.modelo()(perfil_id=Perfil.query.first().id)

    def guardar(self, formulario):
        datos = self.leer(formulario)
        elemento = self.obtener(formulario.get("id", type=int))
        for campo, valor in datos.items():
            setattr(elemento, campo, valor)
        db.session.add(elemento)
        db.session.commit()
        return elemento

    def eliminar(self, id_elemento):
        elemento = db.get_or_404(self.modelo(), id_elemento)
        db.session.delete(elemento)
        db.session.commit()


class GestorPerfil(GestorSeccion):
    def modelo(self):
        return Perfil

    def ancla(self):
        return "acerca"

    def definir_campos(self):
        return {
            "nombre": ("texto", True),
            "titulo": ("texto", False),
            "descripcion": ("texto", False),
            "email": ("texto", False),
            "ubicacion": ("texto", False),
        }

    def obtener(self, id_elemento):
        return Perfil.query.first()

    def eliminar(self, id_elemento):
        raise ErrorDeValidacion("El perfil no se puede eliminar.")


class GestorExperiencia(GestorSeccion):
    def modelo(self):
        return Experiencia

    def ancla(self):
        return "experiencia"

    def definir_campos(self):
        return {
            "empresa": ("texto", True),
            "puesto": ("texto", True),
            "fecha_inicio": ("fecha", False),
            "fecha_fin": ("fecha", False),
            "descripcion": ("texto", False),
        }


class GestorEducacion(GestorSeccion):
    def modelo(self):
        return Educacion

    def ancla(self):
        return "educacion"

    def definir_campos(self):
        return {
            "instituto": ("texto", True),
            "carrera": ("texto", True),
            "fecha_inicio": ("fecha", False),
            "fecha_fin": ("fecha", False),
        }


class GestorHabilidad(GestorSeccion):
    def modelo(self):
        return Habilidad

    def ancla(self):
        return "skills"

    def definir_campos(self):
        return {
            "nombre": ("texto", True),
            "porcentaje": ("entero", True),
            "tipo_id": ("entero", True),
        }

    def validar(self, datos):
        super().validar(datos)
        if not 0 <= datos["porcentaje"] <= 100:
            raise ErrorDeValidacion("El porcentaje debe estar entre 0 y 100.")
        if datos["tipo_id"] not in (1, 2, 3):
            raise ErrorDeValidacion("Tipo de skill inválido.")


class GestorProyecto(GestorSeccion):
    def modelo(self):
        return Proyecto

    def ancla(self):
        return "proyectos"

    def definir_campos(self):
        return {
            "nombre": ("texto", True),
            "fecha": ("fecha", False),
            "descripcion": ("texto", False),
            "link": ("texto", False),
        }


GESTORES = {
    "perfil": GestorPerfil(),
    "experiencia": GestorExperiencia(),
    "educacion": GestorEducacion(),
    "habilidad": GestorHabilidad(),
    "proyecto": GestorProyecto(),
}
