"""
servicios.py
Clase abstracta Servicio y tres servicios especializados:
reserva de salas, alquiler de equipos y asesorías especializadas.
"""
from abc import abstractmethod

from entidades import Entidad
from excepciones import (ServicioInvalidoError, ParametroFaltanteError,
                         CalculoInconsistenteError)


class Servicio(Entidad):
    """Clase abstracta de la que heredan todos los servicios de Software FJ."""

    _familia = "servicio"

    def __init__(self, nombre=None, tarifa_hora=None):
        super().__init__()
        self.nombre = nombre
        self.tarifa_hora = tarifa_hora
        self._disponible = True  # todos los servicios nacen disponibles

    # ---------- nombre ----------
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        self._nombre = str(valor).strip()

    # ---------- tarifa por hora ----------
    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @tarifa_hora.setter
    def tarifa_hora(self, valor):
        if valor is None:
            raise ParametroFaltanteError("La tarifa por hora es obligatoria.")
        try:
            numero = float(valor)  # intenta convertir a número
        except (TypeError, ValueError) as error:
            # Encadenamiento: el error nuevo guarda como causa el error original
            raise ServicioInvalidoError(
                f"La tarifa '{valor}' no es un número.") from error
        if numero <= 0:
            raise ServicioInvalidoError(f"La tarifa debe ser mayor que 0 (llegó {numero}).")
        self._tarifa_hora = numero

    # ---------- disponibilidad ----------
    @property
    def disponible(self):
        return self._disponible

    def marcar_disponible(self, estado):
        """Cambia la disponibilidad del servicio (True o False)."""
        self._disponible = bool(estado)

    # ---------- métodos abstractos (cada servicio los implementa a su manera) ----------
    @abstractmethod
    def validar_parametros(self):
        """Revisa que los datos propios del servicio sean correctos."""
        pass

    @abstractmethod
    def _costo_base(self, horas):
        """Costo sin impuestos ni descuentos. Cambia según el tipo de servicio."""
        pass

    # ---------- método sobrecargado ----------
    def calcular_costo(self, horas, impuesto=None, descuento=None):
        """
        Calcula el costo de la reserva.
        Python no tiene sobrecarga como Java, así que se simula con parámetros opcionales:
          calcular_costo(horas)                       -> costo simple
          calcular_costo(horas, impuesto)             -> costo + impuesto (ej. 0.19)
          calcular_costo(horas, impuesto, descuento)  -> costo + impuesto - descuento
          calcular_costo(horas, descuento=0.10)       -> costo con descuento y sin impuesto
        """
        # Validaciones de los parámetros
        if isinstance(horas, bool) or not isinstance(horas, (int, float)):
            raise CalculoInconsistenteError(f"Las horas deben ser un número (llegó '{horas}').")
        if horas <= 0:
            raise CalculoInconsistenteError(f"Las horas deben ser mayores que 0 (llegó {horas}).")
        if impuesto is not None and not (0 <= impuesto <= 1):
            raise CalculoInconsistenteError(f"Impuesto fuera de rango (0 a 1): {impuesto}.")
        if descuento is not None and not (0 <= descuento <= 1):
            raise CalculoInconsistenteError(f"Descuento fuera de rango (0 a 1): {descuento}.")

        total = self._costo_base(horas)          # costo según el tipo de servicio
        if descuento:                            # si hay descuento, se resta
            total -= total * descuento
        if impuesto:                             # si hay impuesto, se suma
            total += total * impuesto
        if total <= 0:                           # un costo no puede ser cero o negativo
            raise CalculoInconsistenteError(f"El costo calculado no es válido: {total}.")
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio de reserva de salas de reuniones."""

    def __init__(self, nombre=None, tarifa_hora=None, capacidad=None):
        super().__init__(nombre, tarifa_hora)
        self.capacidad = capacidad
        self.validar_parametros()

    def validar_parametros(self):
        if not isinstance(self.capacidad, int) or self.capacidad <= 0:
            raise ServicioInvalidoError(
                f"La capacidad de la sala debe ser un entero positivo (llegó '{self.capacidad}').")

    def _costo_base(self, horas):
        # Las salas grandes (más de 20 personas) tienen un recargo del 15 %
        base = self.tarifa_hora * horas
        return base * 1.15 if self.capacidad > 20 else base

    def describir(self):
        return (f"Sala #{self.id}: {self.nombre} | capacidad {self.capacidad} personas | "
                f"${self.tarifa_hora:,.0f}/hora")


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos (portátiles, proyectores, etc.)."""

    def __init__(self, nombre=None, tarifa_hora=None, tipo_equipo=None, seguro=0):
        super().__init__(nombre, tarifa_hora)
        self.tipo_equipo = tipo_equipo
        self.seguro = seguro  # valor fijo del seguro del equipo
        self.validar_parametros()

    def validar_parametros(self):
        if self.tipo_equipo is None or str(self.tipo_equipo).strip() == "":
            raise ParametroFaltanteError("El tipo de equipo es obligatorio.")
        if not isinstance(self.seguro, (int, float)) or self.seguro < 0:
            raise ServicioInvalidoError(f"El seguro no puede ser negativo (llegó '{self.seguro}').")

    def _costo_base(self, horas):
        # Tarifa por horas más el seguro, que se cobra una sola vez
        return self.tarifa_hora * horas + self.seguro

    def describir(self):
        return (f"Equipo #{self.id}: {self.nombre} ({self.tipo_equipo}) | "
                f"${self.tarifa_hora:,.0f}/hora + seguro ${self.seguro:,.0f}")


class Asesoria(Servicio):
    """Servicio de asesoría especializada."""

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}  # multiplicador por nivel

    def __init__(self, nombre=None, tarifa_hora=None, especialidad=None, nivel="junior"):
        super().__init__(nombre, tarifa_hora)
        self.especialidad = especialidad
        self.nivel = str(nivel).lower()
        self.validar_parametros()

    def validar_parametros(self):
        if self.especialidad is None or str(self.especialidad).strip() == "":
            raise ParametroFaltanteError("La especialidad de la asesoría es obligatoria.")
        if self.nivel not in self.NIVELES:
            raise ServicioInvalidoError(
                f"Nivel '{self.nivel}' no existe. Opciones: {', '.join(self.NIVELES)}.")

    def _costo_base(self, horas):
        return self.tarifa_hora * horas * self.NIVELES[self.nivel]

    def describir(self):
        return (f"Asesoría #{self.id}: {self.nombre} | {self.especialidad} ({self.nivel}) | "
                f"${self.tarifa_hora:,.0f}/hora")
