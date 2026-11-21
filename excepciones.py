"""
excepciones.py
Excepciones personalizadas del sistema Software FJ.
Todas heredan de ErrorSoftwareFJ para poder atraparlas juntas si hace falta.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base de todo el sistema."""

    def __init__(self, mensaje, codigo="FJ-000"):
        super().__init__(mensaje)  # guarda el mensaje en la excepción
        self.codigo = codigo       # código para identificar el tipo de error en el log


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de un cliente no son válidos."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-101")


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando un servicio se crea con parámetros incorrectos."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-201")


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta reservar un servicio que no está disponible."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-202")


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando una reserva tiene datos incorrectos."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-301")


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando se hace algo que el estado de la reserva no permite."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-302")


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando el cálculo de un costo da un resultado que no tiene sentido."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-401")


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un dato obligatorio."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-102")
