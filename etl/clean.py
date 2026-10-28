import pandas as pd

FICHIER = "data/validations-reseau-ferre-nombre-validations-par-jour-4eme-trimestre.csv"


def charger_et_nettoyer():
    df = pd.read_csv(FICHIER, sep=";")

    # 1. Noms de colonnes lisibles
    df = df.rename(columns={
        "JOUR": "jour",
        "CODE_STIF_TRNS": "code_transporteur",
        "CODE_STIF_RES": "code_reseau",
        "CODE_STIF_ARRET": "code_arret",
        "ID_ZDC": "id_zdc",
        "LIBELLE_ARRET": "nom_arret",
        "CATEGORIE_TITRE": "categorie_titre",
        "NB_VALD": "nb_validations",
    })

    # 2. Bons types
    df["jour"] = pd.to_datetime(df["jour"])
    df["id_zdc"] = df["id_zdc"].astype(int)

    # 3. Valeurs plus propres
    df["nom_arret"] = df["nom_arret"].str.strip().str.title()
    df["categorie_titre"] = df["categorie_titre"].replace({"NON DEFINI": "Non défini"})

    return df


if __name__ == "__main__":
    df = charger_et_nettoyer()
    print(df.dtypes)
    print(df.head())