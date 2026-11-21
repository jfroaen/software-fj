"""
logger.py
Configura el archivo de logs donde se guardan los eventos y los errores.
"""
import logging
import os

# Carpeta y archivo del log (se crea solo si no existe)
CARPETA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "software_fj.log")


def obtener_logger():
    """Devuelve el logger del sistema. Si ya estaba configurado, lo reutiliza."""
    logger = logging.getLogger("software_fj")
    if logger.handlers:  # evita duplicar mensajes si se llama varias veces
        return logger

    os.makedirs(CARPETA_LOGS, exist_ok=True)  # crea la carpeta logs si no está
    logger.setLevel(logging.INFO)

    # Formato: fecha, nivel y mensaje
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")

    # Handler que escribe en el archivo (mode="w" para empezar limpio en cada ejecución)
    manejador = logging.FileHandler(ARCHIVO_LOG, mode="w", encoding="utf-8")
    manejador.setFormatter(formato)
    logger.addHandler(manejador)
    return logger


# Logger listo para importar desde los demás módulos
log = obtener_logger()
