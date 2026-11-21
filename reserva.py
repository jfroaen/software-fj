"""
reserva.py
Clase Reserva: une cliente, servicio, duración y estado.
Maneja confirmación, cancelación y procesamiento con excepciones.
"""
from entidades import Entidad
from cliente import Cliente
from servicios import Servicio
from excepciones import (ReservaInvalidaError, ServicioNoDisponibleError,
                         OperacionNoPermitidaError, CalculoInconsistenteError,
                         ErrorSoftwareFJ)
from logger import log

# Estados posibles de una reserva
PENDIENTE = "PENDIENTE"
CONFIRMADA = "CONFIRMADA"
CANCELADA = "CANCELADA"
PROCESADA = "PROCESADA"


class Reserva(Entidad):
    """Una reserva de un cliente para un servicio durante cierta cantidad de horas."""

    _familia = "reserva"

    def __init__(self, cliente, servicio, horas):
        # Validaciones al crear la reserva (antes de asignar el id, para no gastar números)
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un servicio válido.")
        if isinstance(horas, bool) or not isinstance(horas, (int, float)) or horas <= 0:
            raise ReservaInvalidaError(f"Duración inválida: '{horas}'. Debe ser mayor que 0.")
        if horas > 12:
            raise ReservaInvalidaError(f"Una reserva no puede pasar de 12 horas (llegó {horas}).")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible.")

        super().__init__()  # ahora sí se asigna el id
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = PENDIENTE
        self._costo = None  # se calcula al procesar

    # Propiedades de solo lectura (encapsulación)
    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def horas(self):
        return self._horas

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self):
        """Pasa la reserva de PENDIENTE a CONFIRMADA."""
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva #{self.id}: está {self._estado}.")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.nombre}' ya no está disponible.")
        self._estado = CONFIRMADA
        log.info(f"Reserva #{self.id} CONFIRMADA ({self._cliente.nombre} - {self._servicio.nombre}).")

    def cancelar(self):
        """Cancela la reserva si todavía no fue procesada."""
        if self._estado in (CANCELADA, PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar la reserva #{self.id}: está {self._estado}.")
        self._estado = CANCELADA
        log.info(f"Reserva #{self.id} CANCELADA.")

    def procesar(self, impuesto=None, descuento=None):
        """
        Procesa la reserva (calcula el costo y la deja PROCESADA).
        Usa try/except/else/finally y encadenamiento de excepciones.
        """
        try:
            if self._estado != CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se procesan reservas CONFIRMADAS (la #{self.id} está {self._estado}).")
            costo = self._servicio.calcular_costo(self._horas, impuesto, descuento)
        except CalculoInconsistenteError as error:
            # Encadenamiento: se lanza un error de reserva que guarda el error original
            raise ReservaInvalidaError(
                f"No se pudo procesar la reserva #{self.id} por un cálculo inconsistente.") from error
        except ErrorSoftwareFJ:
            raise  # los demás errores del sistema se dejan pasar tal cual
        else:
            # Solo se ejecuta si no hubo ningún error en el try
            self._costo = costo
            self._estado = PROCESADA
            log.info(f"Reserva #{self.id} PROCESADA. Costo total: ${costo:,.2f}.")
            return costo
        finally:
            # Se ejecuta siempre, haya error o no
            log.info(f"Fin del intento de procesar la reserva #{self.id} (estado: {self._estado}).")

    def describir(self):
        costo = f"${self._costo:,.2f}" if self._costo is not None else "sin calcular"
        return (f"Reserva #{self.id} | {self._cliente.nombre} | {self._servicio.nombre} | "
                f"{self._horas} h | {self._estado} | costo: {costo}")
