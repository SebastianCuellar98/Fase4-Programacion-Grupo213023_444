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


# PRUEBA DEL PROGRAMA

id_cliente = int(input("Ingrese el ID del cliente: "))
nombre = input("Ingrese el nombre del cliente: ")
correo = input("Ingrese el correo electrónico: ")

cliente1 = Cliente(id_cliente, nombre, correo)

print(cliente1.describir())


# AGREGO CLASE ABSTRACTA SERVICIO:
print("\n")
class Servicio(Entidad):
    def __init__(self, id, costo_base):
        super().__init__(id)
        self.set_costo_base(costo_base)
    # Getter costo base
    def get_costo_base(self):
        return self.__costo_base
    # Setter costo base con validación
    def set_costo_base(self, costo_base):
        if not isinstance(costo_base, (int, float)) or isinstance(costo_base, bool):
            raise ServicioError("El costo base debe ser un número válido")
        if costo_base < 0:
            raise ServicioError("El costo base del servicio no puede ser negativo")
        self.__costo_base = costo_base
    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass

# SERVICIO 1: RESERVA DE SALA:
class ReservaSala(Servicio):
    def __init__(self, id, costo_base, capacidad, proyector=False):
        super().__init__(id, costo_base)
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise ServicioError("La capacidad de la sala debe ser un entero mayor a cero")
        if not isinstance(proyector, bool):
            raise ServicioError("El proyector debe ser un valor verdadero o falso")
        self.capacidad = capacidad
        self.proyector = proyector
    def calcular_costo(self, horas, descuento=0.0):
        if not isinstance(horas, (int, float)) or isinstance(horas, bool) or horas <= 0:
            raise ServicioError("Las horas de reserva de la sala deben ser mayores a cero")
        if not isinstance(descuento, (int, float)) or isinstance(descuento, bool):
            raise ServicioError("El descuento debe ser un número válido")
        if not (0.0 <= descuento <= 1.0):
            raise ServicioError("El descuento debe estar entre 0.0 y 1.0")
        subtotal = self.get_costo_base() * horas
        if self.proyector:
            subtotal += 30.0  # Costo adicional fijo por uso de proyector
        total = subtotal * (1 - descuento)
        logging.info(f"Cálculo de costo para ReservaSala ID {self.id}: ${total}")
        return round(total, 2)
    def describir(self):
        return (
            f"Servicio [Sala] ID: {self.id} | Costo Base: ${self.get_costo_base()} "
            f"| Capacidad: {self.capacidad} personas | Proyector: {'Sí' if self.proyector else 'No'}"
        )

# SERVICIO 2: ALQUILER DE EQUIPO:
class AlquilerEquipo(Servicio):
    def __init__(self, id, costo_base, tipo_equipo):
        super().__init__(id, costo_base)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioError("El tipo de equipo no puede estar vacío")
        self.tipo_equipo = tipo_equipo
    def calcular_costo(self, dias, seguro=False):
        if not isinstance(dias, (int, float)) or isinstance(dias, bool) or dias <= 0:
            raise ServicioError("Los días de alquiler de equipo deben ser mayores a cero")
        if not isinstance(seguro, bool):
            raise ServicioError("El seguro debe ser un valor verdadero o falso")
        total = self.get_costo_base() * dias
        if seguro:
            total += 15.0 * dias  # Costo diario extra por seguro
        logging.info(f"Cálculo de costo para AlquilerEquipo ID {self.id}: ${total}")
        return round(total, 2)
    def describir(self):
        return (
            f"Servicio [Equipo] ID: {self.id} | Costo Base: ${self.get_costo_base()} "
            f"| Tipo de Equipo: {self.tipo_equipo}"
        )

# SERVICIO 3: ASESORÍA ESPECIALIZADA.
class AsesoriaEspecializada(Servicio):
    def __init__(self, id, costo_base, area_experticia):
        super().__init__(id, costo_base)
        if not isinstance(area_experticia, str) or not area_experticia.strip():
            raise ServicioError("El área de experticia no puede estar vacía")
        self.area_experticia = area_experticia
    def calcular_costo(self, sesiones, nivel_senior=False):
        if not isinstance(sesiones, int) or isinstance(sesiones, bool) or sesiones <= 0:
            raise ServicioError("El número de sesiones de asesoría debe ser mayor a cero")
        if not isinstance(nivel_senior, bool):
            raise ServicioError("El nivel senior debe ser un valor verdadero o falso")
        multiplicador = 1.5 if nivel_senior else 1.0
        total = self.get_costo_base() * sesiones * multiplicador
        logging.info(f"Cálculo de costo para AsesoriaEspecializada ID {self.id}: ${total}")
        return round(total, 2)
    def describir(self):
        return (
            f"Servicio [Asesoría] ID: {self.id} | Costo Base: ${self.get_costo_base()} "
            f"| Área: {self.area_experticia}"
        )
# PRUEBAS DE INTEGRACIÓN DE LOS SERVICIOS:
if __name__ == "__main__":
    try:
        # Probando Servicio 1: Sala
        sala1 = ReservaSala(id=101, costo_base=50.0, capacidad=12, proyector=True)
        print(sala1.describir())
        print(f"Costo total (3 horas, 10% descuento): ${sala1.calcular_costo(3, descuento=0.10)}\n")

        # Probando Servicio 2: Equipo
        equipo1 = AlquilerEquipo(id=102, costo_base=25.0, tipo_equipo="Portátil Core i7")
        print(equipo1.describir())
        print(f"Costo total (4 días con seguro): ${equipo1.calcular_costo(4, seguro=True)}\n")

        # Probando Servicio 3: Asesoría
        asesoria1 = AsesoriaEspecializada(id=103, costo_base=80.0, area_experticia="Arquitectura de Software")
        print(asesoria1.describir())
        print(f"Costo total (2 sesiones, nivel senior): ${asesoria1.calcular_costo(2, nivel_senior=True)}")
    except ServicioError as se:
        print(f"Error en el servicio: {se}")

# AGREGO CLASE RESERVA:
class Reserva(Entidad):
    def __init__(self, id, cliente: Cliente, servicio: Servicio, duracion: int):
        super().__init__(id)
        if not isinstance(cliente, Cliente):
            raise ReservaError("El cliente debe ser un objeto de la clase Cliente")
        if not isinstance(servicio, Servicio):
            raise ReservaError("El servicio debe ser un objeto de la clase Servicio")
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise ReservaError("La duración de la reserva debe ser mayor a cero")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Creada"
        self.costo_total = 0.0

    def confirmar_reserva(self, **kwargs):
        try:
            logging.info(f"Iniciando procesamiento de la reserva ID {self.id}...")
            if self.duracion <= 0:
                raise ValueError("La duración de la reserva debe ser mayor a cero.")
            # Cálculo polimórfico del costo llamando al servicio asignado
            self.costo_total = self.servicio.calcular_costo(self.duracion, **kwargs)
            self.estado = "Confirmada"
        except (ServicioError, ValueError) as ve:
            self.estado = "Fallida"
            logging.error(f"Error lógico al procesar la reserva ID {self.id}: {ve}")

    # Encadenamiento de excepciones (mantiene la trazabilidad del error original)
            raise ReservaError(f"No se pudo confirmar la reserva ID {self.id}") from ve
        except Exception as ex:
            self.estado = "Error Crítico"
            logging.critical(f"Error crítico inesperado en reserva ID {self.id}: {ex}")
            raise ReservaError("Ocurrió un error crítico inesperado en el sistema.") from ex
        else:

    # Se ejecuta únicamente si el bloque try finalizó sin excepciones
            logging.info(f"Reserva ID {self.id} confirmada exitosamente. Costo: ${self.costo_total}")
        finally:

    # Se ejecuta siempre (haya éxito o error), ideal para cierres o logs de cierre
            print(f"[LOG SISTEMA] Finalizó el intento de procesamiento para la reserva ID: {self.id}")
    def cancelar_reserva(self):
        try:
            if self.estado not in ("Creada", "Confirmada"):
                raise ReservaError("No se puede cancelar una reserva en este estado.")
            self.estado = "Cancelada"
            logging.info(f"La reserva ID {self.id} ha sido cancelada exitosamente.")
        except ReservaError as e:
            logging.error(f"Error al intentar cancelar la reserva ID {self.id}: {e}")
            raise
        except Exception as e:
            logging.error(f"Error al intentar cancelar la reserva ID {self.id}: {e}")
            raise ReservaError(f"No fue posible cancelar la reserva ID {self.id}") from e
    def describir(self):
        return (
            f"Reserva ID: {self.id} | Estado: {self.estado} | "
            f"Cliente: {self.cliente.get_nombre()} | "
            f"Servicio: {self.servicio.describir()} | "
            f"Duración: {self.duracion} | Costo Total: ${self.costo_total}"
        )
