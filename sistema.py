"""
sistema.py
Clase SistemaFJ: guarda las listas de clientes, servicios y reservas
y ejecuta cada operación atrapando los errores para que el programa nunca se caiga.
"""
from cliente import Cliente
from reserva import Reserva
from excepciones import ErrorSoftwareFJ
from logger import log


class SistemaFJ:
    """Gestor central. No usa base de datos, solo listas en memoria."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def _ejecutar(self, descripcion, funcion, *args, **kwargs):
        """
        Ejecuta una operación de forma segura.
        Devuelve el resultado, o None si hubo un error (que queda en el log).
        """
        try:
            resultado = funcion(*args, **kwargs)
        except ErrorSoftwareFJ as error:
            # Errores propios del sistema: se registran con su código y su causa (si tiene)
            causa = f" | causa: {error.__cause__!r}" if error.__cause__ else ""
            log.error(f"[{error.codigo}] {descripcion} -> {error}{causa}")
            print(f"   ✗ ERROR controlado ({error.codigo}): {error}")
            return None
        except Exception as error:
            # Cualquier otro error inesperado tampoco tumba el programa
            log.critical(f"[FJ-999] Error inesperado en {descripcion} -> {error!r}")
            print(f"   ✗ ERROR inesperado controlado: {error!r}")
            return None
        else:
            log.info(f"OK: {descripcion}")
            print(f"   ✓ {descripcion}")
            return resultado
        finally:
            log.info(f"--- Fin de la operación: {descripcion}")

    # ---------- operaciones del sistema ----------
    def registrar_cliente(self, **datos):
        cliente = self._ejecutar("Registrar cliente", Cliente, **datos)
        if cliente is not None:
            self.clientes.append(cliente)
        return cliente

    def registrar_servicio(self, clase, **datos):
        servicio = self._ejecutar(f"Crear servicio {clase.__name__}", clase, **datos)
        if servicio is not None:
            self.servicios.append(servicio)
        return servicio

    def crear_reserva(self, cliente, servicio, horas):
        reserva = self._ejecutar("Crear reserva", Reserva, cliente, servicio, horas)
        if reserva is not None:
            self.reservas.append(reserva)
        return reserva

    def confirmar_reserva(self, reserva):
        return self._ejecutar(f"Confirmar reserva #{getattr(reserva, 'id', '?')}", reserva.confirmar)

    def cancelar_reserva(self, reserva):
        return self._ejecutar(f"Cancelar reserva #{getattr(reserva, 'id', '?')}", reserva.cancelar)

    def procesar_reserva(self, reserva, impuesto=None, descuento=None):
        return self._ejecutar(f"Procesar reserva #{getattr(reserva, 'id', '?')}",
                              reserva.procesar, impuesto, descuento)

    def resumen(self):
        """Imprime cómo quedó todo al final."""
        print("\n===== RESUMEN FINAL =====")
        print(f"Clientes registrados : {len(self.clientes)}")
        print(f"Servicios creados    : {len(self.servicios)}")
        print(f"Reservas creadas     : {len(self.reservas)}")
        for r in self.reservas:
            print("  -", r.describir())
