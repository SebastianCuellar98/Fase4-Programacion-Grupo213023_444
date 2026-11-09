"""
Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas
Programación 213023 - UNAD - Fase 4
Proyecto completo en un solo archivo Python.
"""

# ============================================================
# PARTE 1: EXCEPCIONES, ENTIDAD Y LOGS
# ============================================================

import logging
from abc import ABC, abstractmethod

logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)


# ---------------- EXCEPCIONES PERSONALIZADAS ----------------
class ErrorFJ(Exception):
    """Error general del sistema."""


class ClienteError(ErrorFJ):
    """Datos del cliente incorrectos."""


class ServicioError(ErrorFJ):
    """Datos del servicio incorrectos."""


class ReservaError(ErrorFJ):
    """Problema al crear o manejar una reserva."""


# ---------------- CLASE ABSTRACTA GENERAL ----------------
class Entidad(ABC):
    def __init__(self, id):
        self.id = id

    @abstractmethod
    def describir(self):
        pass


# ============================================================
# PARTE 2: CLIENTE
# ============================================================

class Cliente(Entidad):

    def __init__(self, id, nombre, correo, telefono):
        
        if not isinstance(id, int) or id <= 0:
            raise ClienteError(
                "El ID debe ser un número entero mayor que cero"
            )

        super().__init__(id)

        self.set_nombre(nombre)
        self.set_correo(correo)
        self.set_telefono(telefono)

    # =========================
    # NOMBRE
    # =========================

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):

        if not isinstance(nombre, str):
            raise ClienteError(
                "El nombre debe ser texto"
            )

        nombre = nombre.strip()

        if not nombre:
            raise ClienteError(
                "El nombre no puede estar vacío"
            )

        if len(nombre) < 3:
            raise ClienteError(
                "El nombre debe tener al menos 3 caracteres"
            )

        if not nombre.replace(" ", "").isalpha():
            raise ClienteError(
                "El nombre solo debe contener letras"
            )

        self.__nombre = nombre

    # =========================
    # CORREO
    # =========================

    def get_correo(self):
        return self.__correo

    def set_correo(self, correo):

        if not isinstance(correo, str):
            raise ClienteError(
                "El correo debe ser texto"
            )

        correo = correo.strip()

        if " " in correo:
            raise ClienteError(
                "El correo no debe contener espacios"
            )

        if correo.count("@") != 1:
            raise ClienteError(
                "Correo electrónico inválido"
            )

        usuario, dominio = correo.split("@")

        if usuario == "" or "." not in dominio:
            raise ClienteError(
                "Correo electrónico inválido"
            )

        self.__correo = correo

    # =========================
    # TELEFONO
    # =========================

    def get_telefono(self):
        return self.__telefono

    def set_telefono(self, telefono):

        telefono = str(telefono)

        if not telefono.isdigit():
            raise ClienteError(
                "El teléfono solo debe contener números"
            )

        if len(telefono) < 7:
            raise ClienteError(
                "El teléfono debe tener al menos 7 dígitos"
            )

        self.__telefono = telefono

    # =========================
    # ACTUALIZAR DATOS
    # =========================

    def actualizar_correo(self, nuevo_correo):
        self.set_correo(nuevo_correo)

    def actualizar_telefono(self, nuevo_telefono):
        self.set_telefono(nuevo_telefono)

    # =========================
    # DESCRIPCION
    # =========================

    def describir(self):
        return (
            f"Cliente ID: {self.id} | "
            f"Nombre: {self.__nombre} | "
            f"Correo: {self.__correo} | "
            f"Telefono: {self.__telefono}"
        )
        


# ============================================================
# PARTE 3: SERVICIOS
# ============================================================

def es_numero(valor):
    # bool es subclase de int en Python, por eso se excluye.
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


class Servicio(Entidad):
    def __init__(self, id, costo_base, disponible=True):
        super().__init__(id)
        self.set_costo_base(costo_base)
        if not isinstance(disponible, bool):
            raise ServicioError(
                "La disponibilidad debe ser un valor verdadero o falso"
            )
        self.disponible = disponible

    def get_costo_base(self):
        return self.__costo_base

    def set_costo_base(self, costo_base):
        if not es_numero(costo_base):
            raise ServicioError("El costo base debe ser un número válido")
        if costo_base < 0:
            raise ServicioError("El costo base del servicio no puede ser negativo")
        self.__costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass


class ReservaSala(Servicio):
    def __init__(self, id, costo_base, capacidad, proyector=False,
                 disponible=True):
        super().__init__(id, costo_base, disponible)
        if (not isinstance(capacidad, int) or isinstance(capacidad, bool)
                or capacidad <= 0):
            raise ServicioError(
                "La capacidad de la sala debe ser un entero mayor a cero"
            )
        if not isinstance(proyector, bool):
            raise ServicioError("El proyector debe ser un valor verdadero o falso")
        self.capacidad = capacidad
        self.proyector = proyector

    def calcular_costo(self, horas, descuento=0.0):
        if not es_numero(horas) or horas <= 0:
            raise ServicioError(
                "Las horas de reserva de la sala deben ser mayores a cero"
            )
        if not es_numero(descuento):
            raise ServicioError("El descuento debe ser un número válido")
        if not 0.0 <= descuento <= 1.0:
            raise ServicioError("El descuento debe estar entre 0.0 y 1.0")
        subtotal = self.get_costo_base() * horas
        if self.proyector:
            subtotal += 30.0
        total = subtotal * (1 - descuento)
        logging.info(
            "Cálculo de costo para ReservaSala ID %s: $%s", self.id, total
        )
        return round(total, 2)

    def describir(self):
        proyector = "Sí" if self.proyector else "No"
        return (
            f"Servicio [Sala] ID: {self.id} | "
            f"Costo Base: ${self.get_costo_base()} | "
            f"Capacidad: {self.capacidad} personas | Proyector: {proyector}"
        )


class AlquilerEquipo(Servicio):
    def __init__(self, id, costo_base, tipo_equipo, disponible=True):
        super().__init__(id, costo_base, disponible)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioError("El tipo de equipo no puede estar vacío")
        self.tipo_equipo = tipo_equipo.strip()

    def calcular_costo(self, dias, seguro=False):
        if not es_numero(dias) or dias <= 0:
            raise ServicioError(
                "Los días de alquiler de equipo deben ser mayores a cero"
            )
        if not isinstance(seguro, bool):
            raise ServicioError("El seguro debe ser un valor verdadero o falso")
        total = self.get_costo_base() * dias
        if seguro:
            total += 15.0 * dias
        logging.info(
            "Cálculo de costo para AlquilerEquipo ID %s: $%s", self.id, total
        )
        return round(total, 2)

    def describir(self):
        return (
            f"Servicio [Equipo] ID: {self.id} | "
            f"Costo Base: ${self.get_costo_base()} | "
            f"Tipo de Equipo: {self.tipo_equipo}"
        )


class AsesoriaEspecializada(Servicio):
    def __init__(self, id, costo_base, area_experticia, disponible=True):
        super().__init__(id, costo_base, disponible)
        if not isinstance(area_experticia, str) or not area_experticia.strip():
            raise ServicioError("El área de experticia no puede estar vacía")
        self.area_experticia = area_experticia.strip()

    def calcular_costo(self, sesiones, nivel_senior=False):
        if (not isinstance(sesiones, int) or isinstance(sesiones, bool)
                or sesiones <= 0):
            raise ServicioError(
                "El número de sesiones de asesoría debe ser mayor a cero"
            )
        if not isinstance(nivel_senior, bool):
            raise ServicioError(
                "El nivel senior debe ser un valor verdadero o falso"
            )
        multiplicador = 1.5 if nivel_senior else 1.0
        total = self.get_costo_base() * sesiones * multiplicador
        logging.info(
            "Cálculo de costo para AsesoriaEspecializada ID %s: $%s",
            self.id, total
        )
        return round(total, 2)

    def describir(self):
        return (
            f"Servicio [Asesoría] ID: {self.id} | "
            f"Costo Base: ${self.get_costo_base()} | "
            f"Área: {self.area_experticia}"
        )





