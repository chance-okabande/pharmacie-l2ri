from datetime import date
import logging
from models.produit_base import StatutLot

logger = logging.getLogger(__name__)

class Lot:
    """Représente un lot d'un produit avec sa date d'expiration et sa quantité."""

    def __init__(self, numero_lot: str, date_expiration: date, quantite: int):
        self.numero_lot = numero_lot
        self.date_expiration = date_expiration
        self.quantite = quantite
        logger.info(f"Lot créé : {self.numero_lot} — expire le {self.date_expiration}")

    def get_statut(self, seuil_jours: int = 30) -> StatutLot:
        """Retourne le statut du lot selon sa date d'expiration."""
        aujourd_hui = date.today()
        jours_restants = (self.date_expiration - aujourd_hui).days

        if jours_restants < 0:
            return StatutLot.EXPIRE
        elif jours_restants <= seuil_jours:
            return StatutLot.PROCHE_EXPIRATION
        else:
            return StatutLot.VALIDE

    def __str__(self) -> str:
        return (f"Lot {self.numero_lot} | "
                f"Expire : {self.date_expiration} | "
                f"Qté : {self.quantite} | "
                f"Statut : {self.get_statut().value}")