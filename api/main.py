import sqlite3
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Dashboard Transport IDF")

# Autorise le front React (Vite) à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

DB = "data/transport.db"


def requete(sql, params=()):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    lignes = con.execute(sql, params).fetchall()
    con.close()
    return [dict(l) for l in lignes]


@app.get("/stations/top")
def top_stations(limite: int = Query(10, ge=1, le=50)):
    return requete("""
        SELECT a.nom_arret, SUM(v.nb_validations) AS total
        FROM validations v
        JOIN arrets a ON a.arret_id = v.arret_id
        GROUP BY a.nom_arret
        ORDER BY total DESC
        LIMIT ?
    """, (limite,))


@app.get("/validations/par-jour")
def par_jour():
    return requete("""
        SELECT jour, SUM(nb_validations) AS total
        FROM validations
        GROUP BY jour
        ORDER BY jour
    """)


@app.get("/validations/par-titre")
def par_titre():
    return requete("""
        SELECT categorie_titre, SUM(nb_validations) AS total
        FROM validations
        GROUP BY categorie_titre
        ORDER BY total DESC
    """)