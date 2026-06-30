from models.produit_base import ProduitBase, CategorieProduit
from exceptions.exceptions_metier import OrdonnanceManquanteError, RuptureStockError
import logging

logger = logging.getLogger(__name__)

class MedicamentSurOrdonnance(ProduitBase):
    """Médicament vendu uniquement sur présentation d'une ordonnance."""

    def __init__(self, nom: str, code_cip: str, prix: float,
                 quantite_stock: int, categorie: CategorieProduit,
                 substance_active: str):
        super().__init__(nom, code_cip, prix, quantite_stock, categorie)
        self.substance_active = substance_active

    def vendre(self, quantite: int, ordonnance: bool = False) -> None:
        """Vend le médicament si ordonnance valide et stock suffisant."""
        if quantite <= 0:
            raise ValueError(f"La quantité doit être positive, reçu : {quantite}")
        if not ordonnance:
            raise OrdonnanceManquanteError(f"Ordonnance requise pour {self.nom}")
        if quantite > self.quantite_stock:
            raise RuptureStockError(f"Stock insuffisant pour {self.nom}")
        self.quantite_stock -= quantite
        logger.info(f"Vente de {quantite} unité(s) de {self.nom} sur ordonnance")

    def necessite_alerte(self) -> bool:
        """Alerte si stock sous 5 unités."""
        return self.quantite_stock < 5