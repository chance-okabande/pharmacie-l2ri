from datetime import datetime
from models.produit_base import ProduitBase
import logging

logger = logging.getLogger(__name__)

class Vente:
    """Représente une vente enregistrée en pharmacie."""

    def __init__(self, produit: ProduitBase, quantite: int,
                 avec_ordonnance: bool = False):
        self.produit = produit
        self.quantite = quantite
        self.avec_ordonnance = avec_ordonnance
        self.date_vente = datetime.now()
        self.montant_total = produit.prix * quantite
        logger.info(f"Vente enregistrée : {produit.nom} x{quantite} — {self.montant_total} FCFA")