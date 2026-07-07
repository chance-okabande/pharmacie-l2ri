# Pharmacie-L2RI - Gestion de stock de vente

Projet de fin de semestre — Python POO & Persistance  
ISI Dakar — Licence 2 Réseaux Informatiques — 2025-2026  
Formateur : M. HAMANE



## Description

Application console de gestion d'une officine pharmaceutique.  
Elle permet de gérer un catalogue de médicaments et
produits parapharmaceutiques, d'enregistrer des ventes, de détecter les ruptures de stock et les lots proches d'expiration,puis de générer differents rapports.


## Fonctionnalites

- Catalogue mixte : médicaments sur ordonnance, médicaments libres, parapharmacie
- Vente avec contrôle ordonnance et stock
- Détection automatique des lots proches d'expiration
- Alertes de stock bas par type de produit
- Export/import du catalogue en JSON
- Export des ventes en CSV
- Base de données SQLite avec 4 requêtes métier
- Logging complet dans `logs/pharmacie.log`
- Gestion complète des exceptions métier


# Installation

# prerequis
- Python 3.14 ou version superieure

# Cloner le depot
git clone https://github.com/chance-okabande/pharmacie-l2ri.git
cd pharmacie-l2ri

cd pharmacie-l2ri
## Installer les dependances

pip install -r requierements.txt

## Utilisation

python main.py
Les fichiers générés apparaissent dans :
- `data/catalogue.json` → export JSON
- `data/ventes.csv` → export CSV
- `data/pharmacie.db` → base SQLite
- `logs/pharmacie.log` → journal des opérations


## Structure du projet
pharmacie-l2ri/
├── config/
│   └── logging_config.py
├── models/
│   ├── produit_base.py
│   ├── medicament_ordonnance.py
│   ├── medicament_libre.py
│   ├── parapharmacie.py
│   ├── lot.py
│   ├── officine.py
│   └── vente.py
├── persistence/
│   ├── json_manager.py
│   ├── csv_manager.py
│   └── db_manager.py
├── exceptions/
│   └── exceptions_metier.py
├── logs/
├── data/
├── main.py
├── requirements.txt
├── README.md
└── CONTRIBUTIONS.md


## Architecture POO

- `ProduitBase` (ABC) : contrat commun à tous les produits
- `MedicamentSurOrdonnance`, `MedicamentLibre`, `Parapharmacie` : classes filles
- **Composition** : chaque Produit crée et possède ses propres Lot
- **Agrégation** : Officine contient des Produit créés indépendamment
- `CategorieProduit` et `StatutLot` : Enum


## Auteurs

- OKABANDE Chance Erlina — chance-okabande
- BAH Aissatou Bobo — aichaAB92
- KOUMBA Diarisso — koda241