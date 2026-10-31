# Fase4-Programacion-Grupo213023_444
"""
Parte 1 - Excepciones personalizadas, clase abstracta Entidad y configuración de logs
Software FJ - Programación 213023 - UNAD - Fase 4
"""

# Módulo para guardar eventos y errores en un archivo y Herramientas para crear clases abstractas
import logging
from abc import ABC, abstractmethod

# Configuración del archivo de logs (se ejecuta una sola vez al importar este archivo)
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)


# ---------------- EXCEPCIONES PERSONALIZADAS ----------------
class ErrorFJ(Exception):
    """Error general del sistema. Todas las demás heredan de esta."""
    # No necesita código: hereda todo el comportamiento de Exception


class ClienteError(ErrorFJ):
    """Datos del cliente incorrectos."""
    # Se usa cuando el nombre o el correo no son válidos


class ServicioError(ErrorFJ):
    """Datos del servicio incorrectos."""
    # Se usa cuando el precio, las horas o el cálculo no son válidos


class ReservaError(ErrorFJ):
    """Problema al crear o manejar una reserva."""
    # Se usa cuando la reserva no se puede crear, confirmar o cancelar


# ---------------- CLASE ABSTRACTA GENERAL ----------------
class Entidad(ABC):
    def __init__(self, id):
        self.id = id

    @abstractmethod
    def describir(self):
        pass

class Cliente(Entidad):

    def __init__(self, id, nombre, correo):
        super().__init__(id)
        self.set_nombre(nombre)
        self.set_correo(correo)

    # Getter nombre
    def get_nombre(self):
        return self.__nombre

    # Setter nombre con validación
    def set_nombre(self, nombre):
        if not nombre.strip():
            raise ClienteError("El nombre no puede estar vacío")

        if len(nombre.strip()) < 3:
            raise ClienteError(
                "El nombre debe tener al menos 3 caracteres"
            )

        self.__nombre = nombre

    # Getter correo
    def get_correo(self):
        return self.__correo

    # Setter correo con validación
    def set_correo(self, correo):
        if "@" not in correo or "." not in correo:
            raise ClienteError(
                "Correo electrónico inválido"
            )

        self.__correo = correo

    # Método heredado de la clase abstracta
    def describir(self):
        return (
            f"Cliente: {self.__nombre} "
            f"| Correo: {self.__correo}"
        )
        
