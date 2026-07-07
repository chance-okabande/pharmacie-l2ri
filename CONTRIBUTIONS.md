# Contributions au projet

## Membres du groupe

- OKABANDE Chance Erlina — @chance-okabande
- BAH Aissatou Bobo — @aichaAB92
- KOUMBA Diarisso — @koda241

---

## Répartition du travail

| Membre            | Modules / classes développés                                                                        | Contribution |
|-------------------|-----------------------------------------------------------------------------------------------------|--------------|
| Chance Erlina OKABANDE     | `produit_base.py`, `medicament_ordonnance.py`, `lot.py`, `exceptions/`                             | 33%          |
| Aissatou Bobo BAH     | `medicament_libre.py`, `parapharmacie.py`, `vente.py`, `json_manager.py`                           | 33%          |
| KOUMBA Diarisso   | `officine.py`, `csv_manager.py`, `db_manager.py`, `config/`                                        | 34%          |

---

## Répartition par phase

| Phase                             | Responsable principal                         |
|-----------------------------------|-----------------------------------------------|
| Conception (diagramme de classes) | Chance Erlina OKABANDE + Aissatou Bobo BAH + KOUMBA Diarisso      |
| Implémentation POO                | Chance Erlina OKABANDE + Aissatou Bobo BAH                |
| Persistance fichiers (JSON/CSV)   | Aissatou Bobo BAH + KOUMBA Diarisso               |
| Persistance SQL                   | KOUMBA Diarisso                               |
| Tests / gestion des exceptions    | Chance Erlina OKABANDE                               |
| README / documentation            | Chance Erlina OKABANDE + Aissatou Bobo BAH + KOUMBA Diarisso       |

---

## Difficultés rencontrées et résolution

Le sujet lui meme c'est du beton,ca fait mal a la tete

1. **Conflits lors des push simultanés (fetch first)**
   - Difficulté : quand deux membres pushaient en même temps, le dépôt rejetait le push
   - Résolution : utilisation de `git pull --rebase` avant chaque `git push`
   - Résolue par : Chance Erlina OKABANDE + Aissatou Bobo BAH + KOUMBA Diarisso

2. **Reconstruction des objets depuis JSON**
   - Difficulté : recréer la bonne classe fille depuis le champ `type`
   - Résolution : utilisation de `type(produit).__name__` à l'export et `if/elif` à l'import
   - Résolue par : Aissatou Bobo BAH

3. **Gestion des dates en SQLite**
   - Difficulté : SQLite ne possède pas de type DATE natif
   - Résolution : stockage en TEXT au format ISO 8601 avec `strftime` / `fromisoformat`
   - Résolue par : KOUMBA Diarisso