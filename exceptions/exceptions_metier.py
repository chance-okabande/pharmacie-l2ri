import logging

logger = logging.getLogger(__name__)

class OrdonnanceManquanteError(Exception):
    """Levée quand une vente sur ordonnance est tentée sans ordonnance valide."""

    def __init__(self, message: str):
        super().__init__(message)
        logger.warning(f"Ordonnance manquante : {message}")


class RuptureStockError(Exception):
    """Levée quand la quantité demandée dépasse le stock disponible."""

    def __init__(self, message: str):
        super().__init__(message)
        logger.warning(f"Rupture de stock : {message}")