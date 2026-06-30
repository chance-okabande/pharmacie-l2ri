from abc import ABC, abstractmethod
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class CategorieProduit(Enum):
    ANTIBIOTIQUE = "Antibiotique"
    ANTALGIQUE = "Antalgique"
    CHRONIQUE = "Chronique"
    PARAPHARMACIE = "Parapharmacie"
    AUTRE = "Autre"

class StatutLot(Enum):
    VALIDE = "Valide"
    PROCHE_EXPIRATION = "Proche expiration"
    EXPIRE = "Expiré"

class ProduitBase(ABC):
    """Classe abstraite représentant un produit en pharmacie."""

    def __init__(self, nom: str, code_cip: str, prix: float, quantite_stock: int, categorie: CategorieProduit):
        self.nom = nom
        self.code_cip = code_cip
        self.prix = prix
        self.quantite_stock = quantite_stock
        self.categorie = categorie
        self.lots = []
        logger.info(f"Produit créé : {self.nom} ({self.code_cip})")

    @abstractmethod
    def vendre(self, quantite: int) -> None:
        """Effectue la vente d'une quantité donnée."""
        pass

    @abstractmethod
    def necessite_alerte(self) -> bool:
        """Retourne True si le produit nécessite une alerte."""
        pass

    def __str__(self) -> str:
        return f"{self.nom} | {self.code_cip} | {self.prix} FCFA | Stock: {self.quantite_stock}"