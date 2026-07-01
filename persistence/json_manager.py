import json
from datetime import date
import logging

logger = logging.getLogger(__name__)

class JSONManager:
    """Gère la sauvegarde et le chargement du catalogue en JSON."""

    @staticmethod
    def exporter_catalogue(officine, chemin: str) -> None:
        """Exporte le catalogue complet de l'officine en JSON."""
        from models.medicament_ordonnance import MedicamentSurOrdonnance
        from models.medicament_libre import MedicamentLibre
        from models.parapharmacie import Parapharmacie

        try:
            data = {
                "officine": officine.nom,
                "adresse": officine.adresse,
                "produits": []
            }

            for produit in officine.produits:
                produit_data = {
                    "type": type(produit).__name__,
                    "nom": produit.nom,
                    "code_cip": produit.code_cip,
                    "prix": produit.prix,
                    "quantite_stock": produit.quantite_stock,
                    "categorie": produit.categorie.value,
                    "lots": [
                        {
                            "numero_lot": lot.numero_lot,
                            "date_expiration": lot.date_expiration.isoformat(),
                            "quantite": lot.quantite
                        }
                        for lot in produit.lots
                    ]
                }

                if isinstance(produit, MedicamentSurOrdonnance):
                    produit_data["substance_active"] = produit.substance_active
                elif isinstance(produit, MedicamentLibre):
                    produit_data["dose_max_journaliere"] = produit.dose_max_journaliere
                elif isinstance(produit, Parapharmacie):
                    produit_data["marque"] = produit.marque

                data["produits"].append(produit_data)

            with open(chemin, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            logger.info(f"Catalogue exporté vers {chemin}")

        except OSError as e:
            logger.error(f"Erreur lors de l'export JSON : {e}")
            raise

    @staticmethod
    def importer_catalogue(chemin: str):
        """Charge le catalogue depuis un fichier JSON et reconstruit l'officine."""
        from models.officine import Officine
        from models.medicament_ordonnance import MedicamentSurOrdonnance
        from models.medicament_libre import MedicamentLibre
        from models.parapharmacie import Parapharmacie
        from models.produit_base import CategorieProduit

        try:
            with open(chemin, "r", encoding="utf-8") as f:
                data = json.load(f)

            officine = Officine(data["officine"], data["adresse"])

            for p in data["produits"]:
                categorie = CategorieProduit(p["categorie"])

                if p["type"] == "MedicamentSurOrdonnance":
                    produit = MedicamentSurOrdonnance(
                        p["nom"], p["code_cip"], p["prix"],
                        p["quantite_stock"], categorie,
                        p["substance_active"]
                    )
                elif p["type"] == "MedicamentLibre":
                    produit = MedicamentLibre(
                        p["nom"], p["code_cip"], p["prix"],
                        p["quantite_stock"], categorie,
                        p["dose_max_journaliere"]
                    )
                elif p["type"] == "Parapharmacie":
                    produit = Parapharmacie(
                        p["nom"], p["code_cip"], p["prix"],
                        p["quantite_stock"], categorie,
                        p["marque"]
                    )
                else:
                    raise ValueError(f"Type de produit inconnu : {p['type']}")

                for lot in p["lots"]:
                    produit.ajouter_lot(
                        lot["numero_lot"],
                        date.fromisoformat(lot["date_expiration"]),
                        lot["quantite"]
                    )

                officine.ajouter_produit(produit)

            logger.info(f"Catalogue importé depuis {chemin}")
            return officine

        except FileNotFoundError:
            logger.error(f"Fichier introuvable : {chemin}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Fichier JSON invalide : {e}")
            raise