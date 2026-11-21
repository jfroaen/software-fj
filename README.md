# Software FJ - Sistema de gestión de clientes, servicios y reservas

Proyecto de la **Fase 4 - Componente práctico - Prácticas simuladas** del curso Programación (213023A_2204), UNAD.



## Cómo ejecutarlo
Python 3.8 o superior y no necesita instalar nada.

    python main.py

Al correr se hacen 16 operaciones (válidas e inválidas) y se genera `logs/software_fj.log`.

## Estructura
| Archivo | Qué tiene |
|---|---|
| `entidades.py` | Clase abstracta `Entidad` |
| `cliente.py` | `Cliente` con datos encapsulados y validaciones |
| `servicios.py` | Clase abstracta `Servicio` y las clases `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| `reserva.py` | `Reserva`: confirmar, cancelar y procesar |
| `excepciones.py` | Excepciones personalizadas |
| `logger.py` | Configuración del archivo de logs |
| `sistema.py` | `SistemaFJ`: listas y ejecución segura de operaciones |
| `main.py` | Simulación de las operaciones |

## Conceptos aplicados
- **Abstracción:** `Entidad` y `Servicio` son clases abstractas.
- **Herencia y polimorfismo:** los tres servicios sobrescriben `_costo_base`, `describir` y `validar_parametros`.
- **Encapsulación:** atributos privados con propiedades y validación.
- **Sobrecarga:** `calcular_costo(horas)`, `calcular_costo(horas, impuesto)`, `calcular_costo(horas, impuesto, descuento)` mediante parámetros opcionales.
- **Excepciones:** personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento (`raise ... from ...`).
- **Logs:** todo error y evento queda en `logs/software_fj.log`.

## Integrantes
Jhon Fredy Roa Enciso
