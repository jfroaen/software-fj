"""
entidades.py
Clase abstracta que representa las entidades generales del sistema
(clientes, servicios y reservas).
"""
from abc import ABC, abstractmethod
import itertools


class Entidad(ABC):
    """Clase abstracta base. Toda entidad tiene un id único y se puede describir."""

    _contadores = {}   # un contador por tipo de entidad (cliente, servicio, reserva)
    _familia = "entidad"  # cada clase hija indica a qué familia pertenece

    def __init__(self):
        # El id es automático y se numera por familia: cliente 1,2.. servicio 1,2.. reserva 1,2..
        contador = Entidad._contadores.setdefault(self._familia, itertools.count(1))
        self._id = next(contador)

    @property
    def id(self):
        """El id es solo de lectura (encapsulación)."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada entidad debe decir cómo se describe. Es obligatorio sobrescribirlo."""
        pass

    def __str__(self):
        return self.describir()
