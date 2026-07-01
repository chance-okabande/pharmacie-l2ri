from models.produit_base import ProduitBase, CategorieProduit, StatutLot
import logging

logger = logging.getLogger(__name__)

class Officine:
    """Représente la pharmacie qui gère le catalogue de produits."""

    def __init__(self, nom: str, adresse: str):
        self.nom = nom
        self.adresse = adresse
        self.produits: list[ProduitBase] = []
        logger.info(f"Officine créée : {self.nom}")

    def ajouter_produit(self, produit: ProduitBase) -> None:
        """Ajoute un produit existant au catalogue (agrégation)."""
        if not isinstance(produit, ProduitBase):
            raise TypeError("Le produit doit être une instance de ProduitBase")
        self.produits.append(produit)
        logger.info(f"Produit ajouté au catalogue : {produit.nom}")

    def rechercher_par_code(self, code_cip: str) -> ProduitBase:
        """Recherche un produit par son code CIP."""
        for produit in self.produits:
            if produit.code_cip == code_cip:
                return produit
        raise ValueError(f"Aucun produit trouvé avec le code {code_cip}")

    def rechercher_par_categorie(self, categorie: CategorieProduit) -> list:
        """Retourne tous les produits d'une catégorie donnée."""
        return [p for p in self.produits if p.categorie == categorie]

    def produits_en_alerte(self) -> list:
        """Retourne les produits nécessitant une alerte de stock."""
        return [p for p in self.produits if p.necessite_alerte()]

    def produits_lots_expiration(self, statut: StatutLot) -> list:
        """Retourne les produits ayant des lots avec le statut donné."""
        resultats = []
        for produit in self.produits:
            lots = produit.get_lots_par_statut(statut)
            if lots:
                resultats.append((produit, lots))
        return resultats

    def rapport_stock(self) -> None:
        """Affiche un rapport complet de l'état du stock."""
        print(f"\n=== Rapport de stock — {self.nom} ===")
        for produit in self.produits:
            alerte = "ALERTE" if produit.necessite_alerte() else "OK"
            print(f"{produit} | {alerte}")
        print("=" * 50)

    def __str__(self) -> str:
        return f"{self.nom} | {self.adresse} | {len(self.produits)} produit(s)"