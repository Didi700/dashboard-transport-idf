from clean import charger_et_nettoyer

df = charger_et_nettoyer()

# 1. Le couple (code_arret, id_zdc) est-il une clé unique ?
max_noms = df.groupby(["code_arret", "id_zdc"])["nom_arret"].nunique().max()
print("code_arret + id_zdc -> max de noms :", max_noms)

# 2. Pourquoi un id_zdc a-t-il plusieurs noms ?
nb_noms = df.groupby("id_zdc")["nom_arret"].nunique()
ids_multiples = nb_noms[nb_noms > 1].index
print(len(ids_multiples), "id_zdc avec plusieurs noms")

exemple = df[df["id_zdc"].isin(ids_multiples[:5])]
print(exemple[["id_zdc", "code_arret", "nom_arret"]]
      .drop_duplicates().sort_values(["id_zdc", "code_arret"]))