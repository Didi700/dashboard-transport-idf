import sqlite3
import pandas as pd

con = sqlite3.connect("data/transport.db")

# 1. Top 10 des stations les plus fréquentées
q1 = """
SELECT a.nom_arret, SUM(v.nb_validations) AS total
FROM validations v
JOIN arrets a ON a.arret_id = v.arret_id
GROUP BY a.nom_arret
ORDER BY total DESC
LIMIT 10;
"""

# 2. Évolution par jour (toutes stations confondues)
q2 = """
SELECT jour, SUM(nb_validations) AS total
FROM validations
GROUP BY jour
ORDER BY jour;
"""

# 3. Répartition par catégorie de titre
q3 = """
SELECT categorie_titre, SUM(nb_validations) AS total
FROM validations
GROUP BY categorie_titre
ORDER BY total DESC;
"""

for nom, q in [("Top stations", q1), ("Par jour", q2), ("Par titre", q3)]:
    print(f"\n--- {nom} ---")
    print(pd.read_sql_query(q, con).head(10))

con.close()
