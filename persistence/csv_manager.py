import csv
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class CSVManager:
    """Gère l'export des ventes en CSV."""

    @staticmethod
    def exporter_ventes(ventes: list, chemin: str,
                        date_debut: datetime = None,
                        date_fin: datetime = None) -> None:
        """Exporte les ventes d'une période donnée en CSV."""
        try:
            ventes_filtrees = ventes
            if date_debut and date_fin:
                ventes_filtrees = [
                    v for v in ventes
                    if date_debut <= v.date_vente <= date_fin
                ]

            with open(chemin, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "date_vente", "produit", "code_cip", "categorie",
                    "quantite", "prix_unitaire", "montant_total", "avec_ordonnance"
                ])
                writer.writeheader()

                for vente in ventes_filtrees:
                    writer.writerow({
                        "date_vente": vente.date_vente.strftime("%d/%m/%Y %H:%M"),
                        "produit": vente.produit.nom,
                        "code_cip": vente.produit.code_cip,
                        "categorie": vente.produit.categorie.value,
                        "quantite": vente.quantite,
                        "prix_unitaire": vente.produit.prix,
                        "montant_total": vente.montant_total,
                        "avec_ordonnance": "Oui" if vente.avec_ordonnance else "Non"
                    })

            logger.info(f"{len(ventes_filtrees)} vente(s) exportée(s) vers {chemin}")

        except OSError as e:
            logger.error(f"Erreur lors de l'export CSV : {e}")
            raise

    @staticmethod
    def exporter_ventes_du_jour(ventes: list, chemin: str) -> None:
        """Exporte uniquement les ventes du jour en cours."""
        aujourd_hui = datetime.now().date()
        ventes_du_jour = [v for v in ventes if v.date_vente.date() == aujourd_hui]
        CSVManager.exporter_ventes(ventes_du_jour, chemin)
        logger.info(f"Ventes du jour exportées : {len(ventes_du_jour)} vente(s)")