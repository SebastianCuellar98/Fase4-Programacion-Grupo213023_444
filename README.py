"""
Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas
Programación 213023 - UNAD - Fase 4
Proyecto completo en un solo archivo.
"""


# ============================================================
# PARTE 1: EXCEPCIONES, ENTIDAD Y LOGS
# ============================================================

import logging                       # Módulo para guardar eventos y errores en un archivo
from abc import ABC, abstractmethod  # Herramientas para crear clases abstractas

# Configuración del archivo de logs (se ejecuta una sola vez al importar este archivo)
logging.basicConfig(
    filename="software_fj.log",                           # Nombre del archivo de logs
    level=logging.INFO,                                   # Guarda mensajes INFO, WARNING y ERROR
    format="%(asctime)s | %(levelname)s | %(message)s",   # Formato: fecha | nivel | mensaje
    encoding="utf-8",                                     # Permite guardar tildes y ñ
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
class Entidad(ABC):                  # Clase abstracta: no se pueden crear objetos de ella
    def __init__(self, id):          # Constructor que recibe el identificador
        self.id = id                 # Guarda el id de la entidad

    @abstractmethod                  # Obliga a las clases hijas a implementar este método
    def describir(self):             # Método para describir la entidad en texto
        pass                         # Sin código: cada hija lo define


# ============================================================
# PARTE 2: CLIENTE
# ============================================================



class Cliente(Entidad):                         # Cliente hereda de Entidad

    def __init__(self, id, nombre, correo):     # Constructor con los datos del cliente
        super().__init__(id)                    # Guarda el id usando el constructor de Entidad
        self.set_nombre(nombre)                 # Guarda el nombre pasando por su validación
        self.set_correo(correo)                 # Guarda el correo pasando por su validación

    # Getter nombre
    def get_nombre(self):                       # Método para leer el nombre privado
        return self.__nombre                    # Devuelve el nombre

    # Setter nombre con validación
    def set_nombre(self, nombre):               # Método para cambiar el nombre validándolo
        if not isinstance(nombre, str):         # Revisa que el nombre sea texto
            raise ClienteError("El nombre debe ser texto")   # Error si no es texto
        nombre = nombre.strip()                 # Quita espacios al inicio y al final
        if not nombre:                          # Revisa que no quede vacío
            raise ClienteError("El nombre no puede estar vacío")   # Error si está vacío
        if len(nombre) < 3:                     # Revisa que tenga mínimo 3 caracteres
            raise ClienteError("El nombre debe tener al menos 3 caracteres")   # Error si es corto
        self.__nombre = nombre                  # Guarda el nombre en el atributo privado

    # Getter correo
    def get_correo(self):                       # Método para leer el correo privado
        return self.__correo                    # Devuelve el correo

    # Setter correo con validación
    def set_correo(self, correo):               # Método para cambiar el correo validándolo
        if not isinstance(correo, str):         # Revisa que el correo sea texto
            raise ClienteError("El correo debe ser texto")   # Error si no es texto
        correo = correo.strip()                 # Quita espacios al inicio y al final
        if " " in correo or correo.count("@") != 1:   # Sin espacios y con un solo "@"
            raise ClienteError(f"Correo electrónico inválido: {correo}")   # Error si no cumple
        usuario, dominio = correo.split("@")    # Separa lo que va antes y después del "@"
        if usuario == "" or "." not in dominio: # Debe haber usuario y el dominio debe tener punto
            raise ClienteError(f"Correo electrónico inválido: {correo}")   # Error si no cumple
        if dominio.startswith(".") or dominio.endswith("."):   # El dominio no empieza ni termina en punto
            raise ClienteError(f"Correo electrónico inválido: {correo}")   # Error si no cumple
        self.__correo = correo                  # Guarda el correo en el atributo privado

    # Método heredado de la clase abstracta
    def describir(self):                        # Implementa el método abstracto de Entidad
        return (                                # Devuelve un texto con los datos del cliente
            f"Cliente: {self.__nombre} "        # Parte del nombre
            f"| Correo: {self.__correo}"        # Parte del correo
        )


# ============================================================
# PARTE 3: SERVICIOS
# ============================================================



def es_numero(valor):                           # Función auxiliar: dice si algo es un número real
    # bool es subclase de int en Python, por eso se excluye de forma explícita
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


# ---------------- CLASE ABSTRACTA SERVICIO ----------------
class Servicio(Entidad):                        # Servicio hereda de Entidad
    def __init__(self, id, costo_base, disponible=True):   # Constructor general de todo servicio
        super().__init__(id)                    # Guarda el id usando Entidad
        self.set_costo_base(costo_base)         # Guarda el costo base validándolo
        if not isinstance(disponible, bool):    # Revisa que disponible sea verdadero o falso
            raise ServicioError("La disponibilidad debe ser un valor verdadero o falso")  # Error si no
        self.disponible = disponible            # Guarda si el servicio está disponible

    # Getter costo base
    def get_costo_base(self):                   # Método para leer el costo base privado
        return self.__costo_base                # Devuelve el costo base

    # Setter costo base con validación
    def set_costo_base(self, costo_base):       # Método para cambiar el costo base validándolo
        if not es_numero(costo_base):           # Revisa que sea un número
            raise ServicioError("El costo base debe ser un número válido")   # Error si no lo es
        if costo_base < 0:                      # Revisa que no sea negativo
            raise ServicioError("El costo base del servicio no puede ser negativo")  # Error si lo es
        self.__costo_base = costo_base          # Guarda el costo base en el atributo privado

    @abstractmethod                             # Cada servicio hijo debe definir su propio cálculo
    def calcular_costo(self, *args, **kwargs):  # Acepta parámetros distintos según el servicio
        pass                                    # Sin código: lo implementa cada hijo


# ---------------- SERVICIO 1: RESERVA DE SALA ----------------
class ReservaSala(Servicio):                    # ReservaSala hereda de Servicio
    def __init__(self, id, costo_base, capacidad, proyector=False, disponible=True):  # Constructor
        super().__init__(id, costo_base, disponible)   # Guarda id, costo base y disponibilidad
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:  # Valida
            raise ServicioError("La capacidad de la sala debe ser un entero mayor a cero")  # Error
        if not isinstance(proyector, bool):     # Revisa que proyector sea verdadero o falso
            raise ServicioError("El proyector debe ser un valor verdadero o falso")   # Error si no
        self.capacidad = capacidad              # Guarda la capacidad de la sala
        self.proyector = proyector              # Guarda si la sala incluye proyector

    def calcular_costo(self, horas, descuento=0.0):   # Costo según horas y descuento opcional
        if not es_numero(horas) or horas <= 0:  # Las horas deben ser un número positivo
            raise ServicioError("Las horas de reserva de la sala deben ser mayores a cero")  # Error
        if not es_numero(descuento):            # El descuento debe ser un número
            raise ServicioError("El descuento debe ser un número válido")   # Error si no lo es
        if not (0.0 <= descuento <= 1.0):       # El descuento debe estar entre 0 y 1
            raise ServicioError("El descuento debe estar entre 0.0 y 1.0")  # Error si no cumple
        subtotal = self.get_costo_base() * horas   # Subtotal = costo base x horas
        if self.proyector:                      # Si la sala incluye proyector
            subtotal += 30.0                    # Suma un costo adicional fijo por el proyector
        total = subtotal * (1 - descuento)      # Aplica el descuento
        logging.info(f"Cálculo de costo para ReservaSala ID {self.id}: ${total}")   # Guarda en el log
        return round(total, 2)                  # Devuelve el total con 2 decimales

    def describir(self):                        # Implementa la descripción de la sala
        return (                                # Devuelve un texto con los datos de la sala
            f"Servicio [Sala] ID: {self.id} | Costo Base: ${self.get_costo_base()} "
            f"| Capacidad: {self.capacidad} personas | Proyector: {'Sí' if self.proyector else 'No'}"
        )


# ---------------- SERVICIO 2: ALQUILER DE EQUIPO ----------------
class AlquilerEquipo(Servicio):                 # AlquilerEquipo hereda de Servicio
    def __init__(self, id, costo_base, tipo_equipo, disponible=True):   # Constructor
        super().__init__(id, costo_base, disponible)   # Guarda id, costo base y disponibilidad
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():  # Valida el tipo de equipo
            raise ServicioError("El tipo de equipo no puede estar vacío")   # Error si no es válido
        self.tipo_equipo = tipo_equipo          # Guarda el tipo de equipo

    def calcular_costo(self, dias, seguro=False):   # Costo según días y seguro opcional
        if not es_numero(dias) or dias <= 0:    # Los días deben ser un número positivo
            raise ServicioError("Los días de alquiler de equipo deben ser mayores a cero")  # Error
        if not isinstance(seguro, bool):        # El seguro debe ser verdadero o falso
            raise ServicioError("El seguro debe ser un valor verdadero o falso")   # Error si no
        total = self.get_costo_base() * dias    # Total = costo base x días
        if seguro:                              # Si se contrata seguro
            total += 15.0 * dias                # Suma un costo diario extra por el seguro
        logging.info(f"Cálculo de costo para AlquilerEquipo ID {self.id}: ${total}")   # Log
        return round(total, 2)                  # Devuelve el total con 2 decimales

    def describir(self):                        # Implementa la descripción del equipo
        return (                                # Devuelve un texto con los datos del equipo
            f"Servicio [Equipo] ID: {self.id} | Costo Base: ${self.get_costo_base()} "
            f"| Tipo de Equipo: {self.tipo_equipo}"
        )


# ---------------- SERVICIO 3: ASESORÍA ESPECIALIZADA ----------------
class AsesoriaEspecializada(Servicio):          # AsesoriaEspecializada hereda de Servicio
    def __init__(self, id, costo_base, area_experticia, disponible=True):   # Constructor
        super().__init__(id, costo_base, disponible)   # Guarda id, costo base y disponibilidad
        if not isinstance(area_experticia, str) or not area_experticia.strip():  # Valida el área
            raise ServicioError("El área de experticia no puede estar vacía")   # Error si no es válida
        self.area_experticia = area_experticia  # Guarda el área de experticia

    def calcular_costo(self, sesiones, nivel_senior=False):   # Costo según sesiones y nivel
        if not isinstance(sesiones, int) or isinstance(sesiones, bool) or sesiones <= 0:  # Valida
            raise ServicioError("El número de sesiones de asesoría debe ser mayor a cero")  # Error
        if not isinstance(nivel_senior, bool):  # El nivel senior debe ser verdadero o falso
            raise ServicioError("El nivel senior debe ser un valor verdadero o falso")   # Error si no
        multiplicador = 1.5 if nivel_senior else 1.0   # Un asesor senior cuesta 50% más
        total = self.get_costo_base() * sesiones * multiplicador   # Total = costo x sesiones x nivel
        logging.info(f"Cálculo de costo para AsesoriaEspecializada ID {self.id}: ${total}")  # Log
        return round(total, 2)                  # Devuelve el total con 2 decimales

    def describir(self):                        # Implementa la descripción de la asesoría
        return (                                # Devuelve un texto con los datos de la asesoría
            f"Servicio [Asesoría] ID: {self.id} | Costo Base: ${self.get_costo_base()} "
            f"| Área: {self.area_experticia}"
        )




