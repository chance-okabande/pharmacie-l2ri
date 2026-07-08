from config.logging_config import configurer_logging
from models.produit_base import CategorieProduit, StatutLot
from models.medicament_ordonnance import MedicamentSurOrdonnance
from models.medicament_libre import MedicamentLibre
from models.parapharmacie import Parapharmacie
from models.officine import Officine
from models.vente import Vente
from persistence.json_manager import JSONManager
from persistence.csv_manager import CSVManager
from persistence.db_manager import DBManager
from exceptions.exceptions_metier import OrdonnanceManquanteError, RuptureStockError
from datetime import date
import logging

def main():
    # 1. Configuration du logging
    configurer_logging()
    logger = logging.getLogger(__name__)
    logger.info("Démarrage de l'application Pharmacie")

    # 2. Création de l'officine
    officine = Officine("Pharmacie Okabande", "Dakar, Sénégal")

    # 3. Création des produits
    amoxicilline = MedicamentSurOrdonnance(
        nom="Amoxicilline 500mg",
        code_cip="3400935959691",
        prix=3500.0,
        quantite_stock=50,
        categorie=CategorieProduit.ANTIBIOTIQUE,
        substance_active="Amoxicilline"
    )
    paracetamol = MedicamentLibre(
        nom="Paracétamol 1g",
        code_cip="3400936236924",
        prix=1200.0,
        quantite_stock=8,
        categorie=CategorieProduit.ANTALGIQUE,
        dose_max_journaliere="4g/jour"
    )
    metformine = MedicamentSurOrdonnance(
        nom="Metformine 850mg",
        code_cip="3400935959712",
        prix=2800.0,
        quantite_stock=3,
        categorie=CategorieProduit.CHRONIQUE,
        substance_active="Metformine"
    )
    ibuprofene = MedicamentLibre(
        nom="Ibuprofène 400mg",
        code_cip="3400936541230",
        prix=1500.0,
        quantite_stock=25,
        categorie=CategorieProduit.ANTALGIQUE,
        dose_max_journaliere="1200mg/jour"
    )
    doliprane = MedicamentLibre(
        nom="Doliprane 500mg",
        code_cip="3400936541999",
        prix=900.0,
        quantite_stock=2,
        categorie=CategorieProduit.ANTALGIQUE,
        dose_max_journaliere="3g/jour"
    )
    amlodipine = MedicamentSurOrdonnance(
        nom="Amlodipine 5mg",
        code_cip="3400935959800",
        prix=4200.0,
        quantite_stock=15,
        categorie=CategorieProduit.CHRONIQUE,
        substance_active="Amlodipine"
    )
    augmentin = MedicamentSurOrdonnance(
        nom="Augmentin 1g",
        code_cip="3400935959901",
        prix=5500.0,
        quantite_stock=20,
        categorie=CategorieProduit.ANTIBIOTIQUE,
        substance_active="Amoxicilline/Acide clavulanique"
    )
    nivea = Parapharmacie(
        nom="Nivea Crème Hydratante",
        code_cip="3400936999001",
        prix=2500.0,
        quantite_stock=12,
        categorie=CategorieProduit.PARAPHARMACIE,
        marque="Nivea"
    )
    vitamine_c = Parapharmacie(
        nom="Vitamine C 1000mg",
        code_cip="3400936999002",
        prix=3200.0,
        quantite_stock=1,
        categorie=CategorieProduit.PARAPHARMACIE,
        marque="Bayer"
    )
    omega3 = Parapharmacie(
        nom="Oméga 3 Fish Oil",
        code_cip="3400936999003",
        prix=4800.0,
        quantite_stock=7,
        categorie=CategorieProduit.PARAPHARMACIE,
        marque="Solgar"
    )

    # 4. Ajout des lots
    amoxicilline.ajouter_lot("LOT001", date(2026, 8, 15), 30)
    amoxicilline.ajouter_lot("LOT002", date(2026, 7, 10), 20)
    paracetamol.ajouter_lot("LOT003", date(2025, 12, 31), 8)
    metformine.ajouter_lot("LOT004", date(2026, 9, 1), 3)
    nivea.ajouter_lot("LOT005", date(2027, 1, 20), 12)
    vitamine_c.ajouter_lot("LOT006", date(2026, 7, 5), 1)

    # 5. Ajout des produits à l'officine
    for produit in [amoxicilline, paracetamol, metformine, ibuprofene,
                    doliprane, amlodipine, augmentin, nivea, vitamine_c, omega3]:
        officine.ajouter_produit(produit)

    # 6. Rapport de stock initial
    officine.rapport_stock()

    # 7. Simulation des ventes
    ventes = []

    try:
        amoxicilline.vendre(2, ordonnance=True)
        ventes.append(Vente(amoxicilline, 2, avec_ordonnance=True))
    except (OrdonnanceManquanteError, RuptureStockError) as e:
        logger.error(f"Vente échouée : {e}")

    try:
        paracetamol.vendre(3)
        ventes.append(Vente(paracetamol, 3))
    except RuptureStockError as e:
        logger.error(f"Vente échouée : {e}")

    try:
        metformine.vendre(1, ordonnance=False)
    except OrdonnanceManquanteError as e:
        logger.warning(f"Vente refusée (attendu) : {e}")

    try:
        vitamine_c.vendre(10)
    except RuptureStockError as e:
        logger.warning(f"Vente refusée (attendu) : {e}")

    # 8. Produits en alerte stock
    print("\n=== Produits en alerte stock ===")
    for produit in officine.produits_en_alerte():
        print(f"  ALERTE : {produit.nom} — stock : {produit.quantite_stock}")

    # 9. Lots proches expiration
    print("\n=== Lots proches expiration ===")
    for produit, lots in officine.produits_lots_expiration(StatutLot.PROCHE_EXPIRATION):
        for lot in lots:
            print(f"  {produit.nom} — {lot}")

    print("\n=== Lots expirés ===")
    for produit, lots in officine.produits_lots_expiration(StatutLot.EXPIRE):
        for lot in lots:
            print(f"  {produit.nom} — {lot}")

    # 10. Persistance JSON
    JSONManager.exporter_catalogue(officine, "data/catalogue.json")
    officine_rechargee = JSONManager.importer_catalogue("data/catalogue.json")
    logger.info(f"Officine rechargée : {officine_rechargee}")

    # 11. Export CSV
    CSVManager.exporter_ventes_du_jour(ventes, "data/ventes.csv")

    # 12. Base de données
    db = DBManager("data/pharmacie.db")
    for produit in officine.produits:
        db.inserer_produit(produit)
    for vente in ventes:
        db.inserer_vente(vente)

    # 13. Requêtes métier
    print("\n=== Chiffre d'affaires par catégorie ===")
    for row in db.chiffre_affaires_par_categorie():
        print(f"  {row[0]} | {row[1]} vente(s) | {row[2]} FCFA")

    print("\n=== Produits en rupture de stock ===")
    for row in db.produits_en_rupture(seuil=5):
        print(f"  {row[0]} | Stock : {row[3]}")

    print("\n=== Historique ventes Amoxicilline ===")
    for row in db.historique_ventes_produit("3400935959691"):
        print(f"  {row[0]} | Qté : {row[1]} | {row[2]} FCFA | {row[4]}")

    logger.info("Application terminée avec succès")

if __name__ == "__main__":
    main()