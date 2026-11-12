"""
Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas
Programación 213023 - UNAD - Fase 4
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



# ============================================================
# PARTE 2: CLIENTE
# ============================================================

class Cliente(Entidad):                         

    def __init__(self, id, nombre, correo):       # Constructor del cliente
        super().__init__(id)                     # Guarda el ID heredado de Entidad
        self.set_nombre(nombre)                  # Valida y guarda el nombre
        self.set_correo(correo)                  # Valida y guarda el correo

    # Getter nombre
    def get_nombre(self):                       
        return self.__nombre                     # Retorna el nombre del cliente

    # Setter nombre con validación
    def set_nombre(self, nombre):               
        if not isinstance(nombre, str):          # Verifica que el nombre sea texto
            raise ClienteError("El nombre debe ser texto")   
        nombre = nombre.strip()                  # Elimina espacios al inicio y al final
        if not nombre:                           # Verifica que el nombre no esté vacío
            raise ClienteError("El nombre no puede estar vacío")   
        if len(nombre) < 3:                       # Debe tener mínimo 3 caracteres
            raise ClienteError("El nombre debe tener al menos 3 caracteres")   
        self.__nombre = nombre                   # Guarda el nombre validado

    # Getter correo
    def get_correo(self):                       
        return self.__correo                     # Retorna el correo del cliente

    # Setter correo con validación
    def set_correo(self, correo):              
        if not isinstance(correo, str):          # Verifica que el correo sea texto
            raise ClienteError("El correo debe ser texto")   
        correo = correo.strip()                  # Elimina espacios innecesarios
        if " " in correo or correo.count("@") != 1:   
            raise ClienteError(f"Correo electrónico inválido: {correo}")         # Verifica estructura básica del correo
        usuario, dominio = correo.split("@")                                     # Divide el correo en usuario y dominio
        if usuario == "" or "." not in dominio: 
            raise ClienteError(f"Correo electrónico inválido: {correo}")         # Verifica que exista dominio válido
        if dominio.startswith(".") or dominio.endswith("."):   
            raise ClienteError(f"Correo electrónico inválido: {correo}")         # Evita dominios incorrectos  
        self.__correo = correo                                                   # Guarda el correo validado

    # Método heredado de la clase abstracta
    def describir(self):                       
        return (                                
            f"Cliente: {self.__nombre} "                                        # Muestra el nombre del cliente
            f"| Correo: {self.__correo}"                                        # Muestra el correo del cliente
        )



# ============================================================
# PARTE 3: SERVICIOS
# ============================================================

def es_numero(valor):                           
    
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


# ---------------- CLASE ABSTRACTA SERVICIO ----------------
class Servicio(Entidad):                        # Servicio hereda de Entidad
    def __init__(self, id, costo_base, disponible=True):   # Constructor general de todo servicio
        super().__init__(id)                    
        self.set_costo_base(costo_base)         
        if not isinstance(disponible, bool):    
            raise ServicioError("La disponibilidad debe ser un valor verdadero o falso")  
        self.disponible = disponible            

    # Getter costo base
    def get_costo_base(self):                   
        return self.__costo_base                

    # Setter costo base con validación
    def set_costo_base(self, costo_base):       
        if not es_numero(costo_base):     
            raise ServicioError("El costo base debe ser un número válido")   
        if costo_base < 0:                      
            raise ServicioError("El costo base del servicio no puede ser negativo")  
        self.__costo_base = costo_base          

    @abstractmethod                           
    def calcular_costo(self, *args, **kwargs):  
        pass                                    


# ---------------- SERVICIO 1: RESERVA DE SALA ----------------
class ReservaSala(Servicio):                    
    def __init__(self, id, costo_base, capacidad, proyector=False, disponible=True):  
        super().__init__(id, costo_base, disponible)   
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:  
            raise ServicioError("La capacidad de la sala debe ser un entero mayor a cero")  
        if not isinstance(proyector, bool):     
            raise ServicioError("El proyector debe ser un valor verdadero o falso")   
        self.capacidad = capacidad              
        self.proyector = proyector             

    def calcular_costo(self, horas, descuento=0.0):  
        if not es_numero(horas) or horas <= 0:  
            raise ServicioError("Las horas de reserva de la sala deben ser mayores a cero")  
        if not es_numero(descuento):           
            raise ServicioError("El descuento debe ser un número válido")   
        if not (0.0 <= descuento <= 1.0):       
            raise ServicioError("El descuento debe estar entre 0.0 y 1.0")  
        subtotal = self.get_costo_base() * horas   
        if self.proyector:                      
            subtotal += 30.0                    
        total = subtotal * (1 - descuento)     
        logging.info(f"Cálculo de costo para ReservaSala ID {self.id}: ${total}")   
        return round(total, 2)                  

    def describir(self):                        
        return (                                
            f"Servicio [Sala] ID: {self.id} | Costo Base: ${self.get_costo_base()} "
            f"| Capacidad: {self.capacidad} personas | Proyector: {'Sí' if self.proyector else 'No'}"
        )


# ---------------- SERVICIO 2: ALQUILER DE EQUIPO ----------------
class AlquilerEquipo(Servicio):                 
    def __init__(self, id, costo_base, tipo_equipo, disponible=True):   
        super().__init__(id, costo_base, disponible)   
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():  
            raise ServicioError("El tipo de equipo no puede estar vacío")   
        self.tipo_equipo = tipo_equipo          

    def calcular_costo(self, dias, seguro=False):   
        if not es_numero(dias) or dias <= 0:    
            raise ServicioError("Los días de alquiler de equipo deben ser mayores a cero")  
        if not isinstance(seguro, bool):        
            raise ServicioError("El seguro debe ser un valor verdadero o falso")   
        total = self.get_costo_base() * dias    
        if seguro:                              
            total += 15.0 * dias                
        logging.info(f"Cálculo de costo para AlquilerEquipo ID {self.id}: ${total}")   
        return round(total, 2)                  

    def describir(self):                        
        return (                                
            f"Servicio [Equipo] ID: {self.id} | Costo Base: ${self.get_costo_base()} "
            f"| Tipo de Equipo: {self.tipo_equipo}"
        )


# ---------------- SERVICIO 3: ASESORÍA ESPECIALIZADA ----------------
class AsesoriaEspecializada(Servicio):          
    def __init__(self, id, costo_base, area_experticia, disponible=True):   
        super().__init__(id, costo_base, disponible)   
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



# ============================================================
# PARTE 4: RESERVA
# ============================================================

class Reserva(Entidad):                                 # Reserva hereda de Entidad
    def __init__(self, id, cliente, servicio, duracion, **opciones):   # Constructor de la reserva
        super().__init__(id)                            # Guarda el id usando Entidad
        if not isinstance(cliente, Cliente):            # Revisa que haya un cliente válido
            raise ReservaError("La reserva requiere un cliente válido")   # Error si no lo hay
        if not isinstance(servicio, Servicio):          # Revisa que haya un servicio válido
            raise ReservaError("La reserva requiere un servicio válido")  # Error si no lo hay
        if not es_numero(duracion) or duracion <= 0:    # La duración debe ser un número positivo
            raise ReservaError("La duración debe ser un número mayor a cero")   # Error si no
        self.cliente = cliente                          # Guarda el cliente
        self.servicio = servicio                        # Guarda el servicio
        self.duracion = duracion                        # Guarda la duración (horas, días o sesiones)
        self.opciones = opciones                        # Guarda opciones: descuento, seguro, etc.
        self.estado = "PENDIENTE"                       # Estado inicial de toda reserva
        self.total = None                               # El total se calcula al procesar

    def confirmar(self):                                # Confirma la reserva
        if self.estado != "PENDIENTE":                  # Solo se confirman reservas pendientes
            raise ReservaError(f"No se puede confirmar una reserva {self.estado}")   # Error si no
        if not self.servicio.disponible:                # Revisa que el servicio esté disponible
            raise ReservaError("El servicio no está disponible")   # Error si no lo está
        self.estado = "CONFIRMADA"                      # Cambia el estado a confirmada

    def cancelar(self):                                 # Cancela la reserva
        if self.estado == "CANCELADA":                  # Revisa que no esté ya cancelada
            raise ReservaError("La reserva ya estaba cancelada")   # Error si ya lo estaba
        self.estado = "CANCELADA"                       # Cambia el estado a cancelada

    def procesar(self):                                 # Procesa la reserva completa
        try:                                            # Intenta ejecutar los pasos
            self.confirmar()                            # Paso 1: confirmar la reserva
            total = self.servicio.calcular_costo(self.duracion, **self.opciones)   # Paso 2: costo
        except (ServicioError, TypeError) as e:         # Falla por parámetros o por opciones erróneas
            self.estado = "PENDIENTE"                   # Revierte el estado de la reserva
            # Encadenamiento de excepciones: se lanza un error nuevo guardando la causa original
            raise ReservaError("No se pudo procesar la reserva") from e
        else:                                           # Solo se ejecuta si no hubo errores
            self.total = total                          # Guarda el total calculado
            logging.info(f"Reserva {self.id} procesada. Total: {total}")   # Guarda el éxito en el log
            return total                                # Devuelve el total
        finally:                                        # Se ejecuta siempre, con o sin error
            logging.info(f"Terminó el proceso de la reserva {self.id} (estado: {self.estado})")  # Log

    def describir(self):                                # Implementa la descripción de la reserva
        return (                                        # Devuelve un texto con los datos
            f"Reserva {self.id} | {self.cliente.get_nombre()} | "
            f"{type(self.servicio).__name__} | duración: {self.duracion} | {self.estado}"
        )



# ============================================================
# PARTE 5: SIMULACIÓN (MAIN)
# ============================================================

# ---------------- LISTAS (en lugar de base de datos) ----------------
clientes = []                                               # Clientes registrados
servicios = []                                              # Servicios creados
reservas = []                                               # Reservas exitosas


def operacion(titulo, funcion):                             # Ejecuta una operación de forma segura
    """Si la operación falla, guarda el error y el programa sigue."""
    print(f"\n{titulo}")                                    # Muestra el título de la operación
    try:                                                    # Intenta ejecutar la operación
        resultado = funcion()                               # Ejecuta la función recibida
    except ErrorFJ as e:                                    # Errores propios del sistema
        logging.error(f"{titulo}: {e} | causa: {e.__cause__}")   # Guarda el error y su causa
        print("  ERROR:", e)                               # Muestra el error en pantalla
        if e.__cause__:                                     # Si el error trae una causa encadenada
            print("  Causa:", e.__cause__)                 # También la muestra
    except Exception as e:                                  # Cualquier otro error inesperado
        logging.error(f"{titulo}: error inesperado {e!r}")  # Guarda el error inesperado
        print("  ERROR INESPERADO:", repr(e))              # Muestra el error en pantalla
    else:                                                   # Si no hubo ningún error
        logging.info(f"{titulo}: OK")                       # Guarda que salió bien
        print("  OK:", resultado)                          # Muestra el resultado
    finally:                                                # Se ejecuta siempre
        print("  (fin de la operación)")                    # Indica que terminó la operación


# ---------------- FUNCIONES PARA LAS PRUEBAS ----------------
def registrar_cliente(nombre, correo):                      # Crea y guarda un cliente
    c = Cliente(len(clientes) + 1, nombre, correo)          # Crea el cliente (puede lanzar error)
    clientes.append(c)                                      # Lo guarda en la lista
    return c.describir()                                    # Devuelve su descripción


def registrar_servicio(clase, *datos, **opciones):          # Crea y guarda un servicio de cualquier tipo
    s = clase(len(servicios) + 1, *datos, **opciones)       # Crea el servicio (puede lanzar error)
    servicios.append(s)                                     # Lo guarda en la lista
    return s.describir()                                    # Devuelve su descripción


def hacer_reserva(num_cliente, num_servicio, duracion, **opciones):   # Crea y procesa una reserva
    try:                                                    # Intenta buscar cliente y servicio
        cliente = clientes[num_cliente]                     # Busca el cliente por posición
        servicio = servicios[num_servicio]                  # Busca el servicio por posición
    except IndexError as e:                                 # Si la posición no existe en la lista
        raise ReservaError("Cliente o servicio no existe") from e   # Error propio con la causa
    r = Reserva(len(reservas) + 1, cliente, servicio, duracion, **opciones)   # Crea la reserva
    total = r.procesar()                                    # La procesa (puede lanzar error)
    reservas.append(r)                                      # Solo se guarda si todo salió bien
    return f"{r.describir()} | Total: ${total}"             # Devuelve la descripción y el total


def cancelar_dos_veces():                                   # Prueba de operación no permitida
    reservas[0].cancelar()                                  # Primera cancelación: funciona
    reservas[0].cancelar()                                  # Segunda cancelación: lanza error


# ---------------- PROGRAMA PRINCIPAL ----------------
def main():                                                 # Función principal
    logging.info("Inicio de la simulación de Software FJ")  # Guarda el inicio en el log

    # --- Clientes (válidos e inválidos) ---
    operacion("1. Registrar cliente válido", lambda: registrar_cliente("Ana Gómez", "ana@correo.com"))
    operacion("2. Registrar cliente con correo inválido", lambda: registrar_cliente("Luis Pérez", "luis@"))
    operacion("3. Registrar cliente con nombre vacío", lambda: registrar_cliente("   ", "sin@correo.com"))
    operacion("4. Registrar cliente con nombre numérico", lambda: registrar_cliente(12345, "num@correo.com"))

    # --- Servicios (válidos e inválidos) ---
    operacion("5. Crear sala válida", lambda: registrar_servicio(ReservaSala, 50.0, 12, proyector=True))
    operacion("6. Crear equipo con costo negativo", lambda: registrar_servicio(AlquilerEquipo, -25.0, "Portátil"))
    operacion("7. Crear asesoría válida", lambda: registrar_servicio(AsesoriaEspecializada, 80.0, "Arquitectura de Software"))
    operacion("8. Crear equipo válido pero no disponible", lambda: registrar_servicio(AlquilerEquipo, 25.0, "Proyector", disponible=False))

    # --- Reservas exitosas ---
    operacion("9. Reserva de sala: 3 horas con 10% de descuento", lambda: hacer_reserva(0, 0, 3, descuento=0.10))
    operacion("10. Reserva de asesoría: 2 sesiones nivel senior", lambda: hacer_reserva(0, 1, 2, nivel_senior=True))

    # --- Reservas fallidas ---
    operacion("11. Reserva de equipo no disponible", lambda: hacer_reserva(0, 2, 4, seguro=True))
    operacion("12. Reserva de sala con descuento fuera de rango", lambda: hacer_reserva(0, 0, 2, descuento=1.5))
    operacion("13. Reserva de asesoría con opción que no le corresponde", lambda: hacer_reserva(0, 1, 2, descuento=0.2))
    operacion("14. Reserva con duración de cero horas", lambda: hacer_reserva(0, 0, 0))
    operacion("15. Reserva con cliente que no existe", lambda: hacer_reserva(99, 0, 2))

    # --- Operación no permitida ---
    operacion("16. Cancelar dos veces la misma reserva", cancelar_dos_veces)

    print("\n----- RESUMEN -----")                           # Título del resumen final
    print("Clientes registrados:", len(clientes))            # Cantidad de clientes
    print("Servicios creados:", len(servicios))              # Cantidad de servicios
    print("Reservas exitosas:", len(reservas))               # Cantidad de reservas exitosas
    for r in reservas:                                       # Recorre las reservas guardadas
        print(" -", r.describir(), "| Total:", r.total)      # Muestra cada reserva
    print("El programa terminó sin detenerse. Revise software_fj.log")   # Mensaje final
    logging.info("Fin de la simulación de Software FJ")      # Guarda el fin en el log


if __name__ == "__main__":                                   # Solo corre si se ejecuta este archivo
    main()                                                   # Llama a la función principal
