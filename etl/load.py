import sqlite3
from clean import charger_et_nettoyer

DB = "data/transport.db"

SCHEMA = """
DROP TABLE IF EXISTS validations;
DROP TABLE IF EXISTS arrets;

CREATE TABLE arrets (
    arret_id   INTEGER PRIMARY KEY,
    code_arret TEXT NOT NULL,
    id_zdc     INTEGER NOT NULL,
    nom_arret  TEXT NOT NULL,
    UNIQUE (code_arret, id_zdc)
);

CREATE TABLE validations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    jour            TEXT NOT NULL,
    arret_id        INTEGER NOT NULL,
    categorie_titre TEXT NOT NULL,
    nb_validations  INTEGER NOT NULL,
    FOREIGN KEY (arret_id) REFERENCES arrets (arret_id)
);

CREATE INDEX idx_valid_jour  ON validations (jour);
CREATE INDEX idx_valid_arret ON validations (arret_id);
"""


def main():
    df = charger_et_nettoyer()

    # Table des arrêts : un arrêt = un couple (code_arret, id_zdc)
    arrets = (df[["code_arret", "id_zdc", "nom_arret"]]
              .drop_duplicates(subset=["code_arret", "id_zdc"])
              .reset_index(drop=True))
    arrets["arret_id"] = arrets.index + 1

    # Table des validations : on remplace l'arrêt par son arret_id
    validations = df.merge(arrets[["arret_id", "code_arret", "id_zdc"]],
                           on=["code_arret", "id_zdc"])
    validations = validations[["jour", "arret_id", "categorie_titre", "nb_validations"]].copy()
    validations["jour"] = validations["jour"].dt.strftime("%Y-%m-%d")

    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)
    arrets.to_sql("arrets", con, if_exists="append", index=False)
    validations.to_sql("validations", con, if_exists="append", index=False, chunksize=50000)
    con.commit()

    print("arrets :", con.execute("SELECT COUNT(*) FROM arrets").fetchone()[0])
    print("validations :", con.execute("SELECT COUNT(*) FROM validations").fetchone()[0])
    print("total CSV :", df["nb_validations"].sum())
    print("total SQL :", con.execute("SELECT SUM(nb_validations) FROM validations").fetchone()[0])
    con.close()


if __name__ == "__main__":
    main()