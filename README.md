# Software FJ — Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto colaborativo correspondiente a la **Fase 4 – Componente práctico (Prácticas simuladas)** del curso **Programación (213023)** de la Universidad Nacional Abierta y a Distancia (UNAD), Grupo **213023_444**.

## Descripción
Aplicación orientada a objetos en **Python** (sin base de datos; gestión mediante objetos, listas en memoria y registro en archivo de logs) que implementa:

- **Abstracción, herencia, encapsulación y polimorfismo**:
  - Clase abstracta `Entidad`
  - Clase `Cliente` con encapsulación y validaciones estrictas de nombre y correo
  - Clase abstracta `Servicio` y tres especializaciones: `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`
  - Clase `Reserva` con ciclo de vida (`PENDIENTE`, `CONFIRMADA`, `CANCELADA`), confirmación, cancelación y procesamiento
  - Métodos sobrecargados mediante parámetros opcionales (`descuento`, `seguro`, `nivel_senior`, `impuesto`)
- **Manejo robusto de excepciones**:
  - Jerarquía personalizada: `ErrorFJ` → `ClienteError`, `ServicioError`, `ReservaError`
  - Uso de `try/except`, `try/except/else`, `try/except/finally` y encadenamiento de excepciones (`raise ... from e`)
  - Registro automático de eventos y errores en `software_fj.log`

## Ejecución
Requiere **Python 3.10+**:

```bash
python README.py
```

Al ejecutarse, el programa simula **21 operaciones completas** (registros válidos e inválidos de clientes, creación de servicios, reservas exitosas y fallidas, cálculo con impuestos/descuentos y control de estados) sin detenerse ante errores, dejando el detalle en `software_fj.log`.

## Estructura del código (`README.py`)
| Parte | Componente | Descripción |
| --- | --- | --- |
| Parte 1 | Excepciones, `Entidad` y Logs | Jerarquía de excepciones personalizadas, clase abstracta base y configuración de `logging` |
| Parte 2 | `Cliente` | Encapsulación de datos personales, getters/setters y validaciones |
| Parte 3 | `Servicio` y subclases | `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` con polimorfismo y cálculo de costos |
| Parte 4 | `Reserva` | Integración de cliente y servicio, estados, confirmación, cancelación y procesamiento con encadenamiento |
| Parte 5 | Simulación y Pruebas (`main`) | Ejecución controlada de 21 escenarios válidos y de error, resumen final y documentación del repositorio |

## Integrantes — Grupo 213023_444
- Jhoan Sebastian Cuellar Galindo
- Maicol Bocanegra Tavera
- Jorge Peña Ramon
- Diego Francisco Barrios Salcedo
- Johnny Muñoz Hernández (`@darksidesad`) — Parte 5: Simulación, pruebas complementarias de excepciones, documentación línea por línea y `README.md`
