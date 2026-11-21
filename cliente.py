"""
cliente.py
Clase Cliente con validaciones y datos personales encapsulados.
"""
import re

from entidades import Entidad
from excepciones import ClienteInvalidoError, ParametroFaltanteError

# Expresión sencilla para revisar que el correo tenga formato correcto
PATRON_CORREO = re.compile(r"^[\w\.\-]+@[\w\-]+(\.[\w\-]+)+$")


class Cliente(Entidad):
    """Cliente de Software FJ. Los datos son privados y se validan al asignarlos."""

    _familia = "cliente"

    def __init__(self, nombre=None, documento=None, correo=None, telefono=None):
        super().__init__()
        # Se usan los setters (propiedades) para que siempre pasen por la validación
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---------- nombre ----------
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre inválido: '{valor}'. Mínimo 3 letras.")
        if any(c.isdigit() for c in valor):
            raise ClienteInvalidoError(f"El nombre no puede tener números: '{valor}'.")
        self._nombre = valor.strip().title()

    # ---------- documento ----------
    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El documento del cliente es obligatorio.")
        texto = str(valor).strip()
        if not texto.isdigit() or not (6 <= len(texto) <= 12):
            raise ClienteInvalidoError(
                f"Documento inválido: '{valor}'. Debe tener entre 6 y 12 números.")
        self._documento = texto

    # ---------- correo ----------
    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El correo del cliente es obligatorio.")
        if not PATRON_CORREO.match(str(valor).strip()):
            raise ClienteInvalidoError(f"Correo con formato inválido: '{valor}'.")
        self._correo = str(valor).strip().lower()

    # ---------- teléfono ----------
    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        texto = str(valor).strip()
        if not texto.isdigit() or len(texto) != 10:
            raise ClienteInvalidoError(
                f"Teléfono inválido: '{valor}'. Debe tener 10 números.")
        self._telefono = texto

    def describir(self):
        """Descripción corta del cliente (sobrescribe el método abstracto)."""
        return f"Cliente #{self.id}: {self.nombre} | CC {self.documento} | {self.correo}"
