import sqlite3
import logging

logger = logging.getLogger(__name__)

class DBManager:
    """Gère la persistance SQL du projet pharmacie."""

    def __init__(self, chemin_db: str):
        self.chemin_db = chemin_db
        self._initialiser_base()

    def _initialiser_base(self) -> None:
        """Crée les tables si elles n'existent pas encore."""
        try:
            with sqlite3.connect(self.chemin_db) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS produits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT NOT NULL,
                        code_cip TEXT UNIQUE NOT NULL,
                        prix REAL NOT NULL,
                        quantite_stock INTEGER NOT NULL,
                        categorie TEXT NOT NULL,
                        type_produit TEXT NOT NULL
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ventes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        produit_id INTEGER NOT NULL,
                        quantite INTEGER NOT NULL,
                        montant_total REAL NOT NULL,
                        avec_ordonnance INTEGER NOT NULL,
                        date_vente TEXT NOT NULL,
                        FOREIGN KEY (produit_id) REFERENCES produits(id)
                    )
                """)
                conn.commit()
                logger.info("Base de données initialisée")
        except sqlite3.Error as e:
            logger.error(f"Erreur initialisation base : {e}")
            raise

    def inserer_produit(self, produit) -> None:
        """Insère un produit dans la base de données."""
        try:
            with sqlite3.connect(self.chemin_db) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR IGNORE INTO produits 
                    (nom, code_cip, prix, quantite_stock, categorie, type_produit)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    produit.nom, produit.code_cip, produit.prix,
                    produit.quantite_stock, produit.categorie.value,
                    type(produit).__name__
                ))
                conn.commit()
                logger.info(f"Produit inséré en base : {produit.nom}")
        except sqlite3.Error as e:
            logger.error(f"Erreur insertion produit : {e}")
            raise

    def inserer_vente(self, vente) -> None:
        """Insère une vente en base après avoir récupéré l'id du produit."""
        try:
            with sqlite3.connect(self.chemin_db) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id FROM produits WHERE code_cip = ?",
                    (vente.produit.code_cip,)
                )
                row = cursor.fetchone()
                if not row:
                    raise ValueError(f"Produit introuvable en base : {vente.produit.code_cip}")

                cursor.execute("""
                    INSERT INTO ventes 
                    (produit_id, quantite, montant_total, avec_ordonnance, date_vente)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    row[0], vente.quantite, vente.montant_total,
                    1 if vente.avec_ordonnance else 0,
                    vente.date_vente.strftime("%Y-%m-%d %H:%M:%S")
                ))
                conn.commit()
                logger.info(f"Vente insérée en base : {vente.produit.nom}")
        except sqlite3.Error as e:
            logger.error(f"Erreur insertion vente : {e}")
            raise

    def chiffre_affaires_par_categorie(self) -> list:
        """Requête métier — CA total par catégorie de produit."""
        try:
            with sqlite3.connect(self.chemin_db) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT p.categorie, COUNT(v.id) AS nombre_ventes,
                           SUM(v.montant_total) AS chiffre_affaires
                    FROM ventes v
                    JOIN produits p ON v.produit_id = p.id
                    GROUP BY p.categorie
                    ORDER BY chiffre_affaires DESC
                """)
                resultats = cursor.fetchall()
                logger.info("Requête CA par catégorie exécutée")
                return resultats
        except sqlite3.Error as e:
            logger.error(f"Erreur requête CA : {e}")
            raise

    def produits_en_rupture(self, seuil: int = 0) -> list:
        """Requête métier — produits sous le seuil de stock."""
        try:
            with sqlite3.connect(self.chemin_db) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT nom, code_cip, categorie, quantite_stock
                    FROM produits
                    WHERE quantite_stock <= ?
                    ORDER BY quantite_stock ASC
                """, (seuil,))
                resultats = cursor.fetchall()
                logger.info(f"Requête rupture stock exécutée — seuil : {seuil}")
                return resultats
        except sqlite3.Error as e:
            logger.error(f"Erreur requête rupture : {e}")
            raise

    def historique_ventes_produit(self, code_cip: str) -> list:
        """Requête métier — historique des ventes d'un produit."""
        try:
            with sqlite3.connect(self.chemin_db) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT p.nom, v.quantite, v.montant_total, v.avec_ordonnance, v.date_vente
                    FROM ventes v
                    JOIN produits p ON v.produit_id = p.id
                    WHERE p.code_cip = ?
                    ORDER BY v.date_vente DESC
                """, (code_cip,))
                resultats = cursor.fetchall()
                logger.info(f"Historique ventes récupéré pour {code_cip}")
                return resultats
        except sqlite3.Error as e:
            logger.error(f"Erreur requête historique : {e}")
            raise