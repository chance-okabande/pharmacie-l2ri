from models.produit_base import ProduitBase, CategorieProduit
from exceptions.exceptions_metier import RuptureStockError
import logging

logger = logging.getLogger(__name__)

class Parapharmacie(ProduitBase):
    """Produit parapharmaceutique : cosmétique, complément alimentaire, etc."""

    def __init__(self, nom: str, code_cip: str, prix: float,
                 quantite_stock: int, categorie: CategorieProduit,
                 marque: str):
        super().__init__(nom, code_cip, prix, quantite_stock, categorie)
        self.marque = marque

    def vendre(self, quantite: int) -> None:
        """Vend le produit si stock suffisant."""
        if quantite <= 0:
            raise ValueError(f"La quantité doit être positive, reçu : {quantite}")
        if quantite > self.quantite_stock:
            raise RuptureStockError(f"Stock insuffisant pour {self.nom}")
        self.quantite_stock -= quantite
        logger.info(f"Vente de {quantite} unité(s) de {self.nom} ({self.marque})")

    def necessite_alerte(self) -> bool:
        """Alerte si stock sous 3 unités."""
        return self.quantite_stock < 3