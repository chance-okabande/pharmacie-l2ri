import logging
from pathlib import Path

def configurer_logging(niveau: str = "INFO") -> None:
    """Configure le système de logging pour toute l'application."""

    Path("logs").mkdir(exist_ok=True)

    format_log = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format = "%d/%m/%Y %H:%M:%S"

    formatter = logging.Formatter(format_log, datefmt=date_format)

    handler_console = logging.StreamHandler()
    handler_console.setLevel(logging.INFO)
    handler_console.setFormatter(formatter)

    handler_fichier = logging.FileHandler("logs/pharmacie.log", encoding="utf-8")
    handler_fichier.setLevel(logging.DEBUG)
    handler_fichier.setFormatter(formatter)

    logging.basicConfig(level=logging.DEBUG, handlers=[handler_console, handler_fichier])
    logging.info("Logging configuré avec succès")