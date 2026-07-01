from models.produit_base import ProduitBase, CategorieProduit
from exceptions.exceptions_metier import RuptureStockError
import logging

logger = logging.getLogger(__name__)

class MedicamentLibre(ProduitBase):
    """Médicament vendu librement sans ordonnance."""

    def __init__(self, nom: str, code_cip: str, prix: float,
                 quantite_stock: int, categorie: CategorieProduit,
                 dose_max_journaliere: str):
        super().__init__(nom, code_cip, prix, quantite_stock, categorie)
        self.dose_max_journaliere = dose_max_journaliere

    def vendre(self, quantite: int) -> None:
        """Vend le médicament si stock suffisant."""
        if quantite <= 0:
            raise ValueError(f"La quantité doit être positive, reçu : {quantite}")
        if quantite > self.quantite_stock:
            raise RuptureStockError(f"Stock insuffisant pour {self.nom}")
        self.quantite_stock -= quantite
        logger.info(f"Vente de {quantite} unité(s) de {self.nom}")

    def necessite_alerte(self) -> bool:
        """Alerte si stock sous 10 unités."""
        return self.quantite_stock < 10