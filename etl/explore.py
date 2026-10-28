import pandas as pd

df = pd.read_csv("data/validations-reseau-ferre-nombre-validations-par-jour-4eme-trimestre.csv", sep=";")

print(df.shape)
print(df.head())
print(df.dtypes)
print(df.isna().sum())

print(df["JOUR"].min(), df["JOUR"].max())
print(df["CATEGORIE_TITRE"].value_counts())
print(df["LIBELLE_ARRET"].nunique(), "arrêts différents")
print(df["NB_VALD"].describe())
print(df.duplicated().sum(), "doublons")
print(df.groupby("LIBELLE_ARRET")["NB_VALD"].sum().sort_values(ascending=False).head(10))