"""
simuler_data_drift.py (bonus, hors évaluation)
────────────────────────────────────────────────
Génère un second jeu de données d'affluence avec une distribution horaire
différente (heures de pointe décalées de 2h — scénario : généralisation des
horaires flexibles dans les entreprises et administrations de Lomé), charge
le modèle actuellement en Production depuis le MLflow Model Registry, et
compare son erreur sur la distribution d'origine vs la distribution décalée.

Aucune exception n'est levée : le modèle répond à chaque requête, il se
trompe simplement davantage. C'est ça, le data drift.
"""

import csv
import random

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score

random.seed(99)

LIGNES = [f"L{i:02d}" for i in range(1, 13)]
HEURES = list(range(5, 23))

# Heures de pointe décalées de ~2h par rapport au dataset d'entraînement
# (7-9h/17-19h à l'origine -> 9-11h/19-21h ici)
HEURES_POIDS_DRIFT = {
    5: 1, 6: 2, 7: 5, 8: 8, 9: 15, 10: 18, 11: 10, 12: 7,
    13: 6, 14: 5, 15: 5, 16: 6, 17: 8, 18: 12, 19: 17,
    20: 18, 21: 6, 22: 3,
}


def generer_dataset_drift(chemin="dataset_affluence_drift.csv"):
    with open(chemin, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ligne_id", "heure", "nb_passagers"])
        for ligne in LIGNES:
            niveau_base_ligne = random.uniform(0.7, 1.4)
            for heure in HEURES:
                for _ in range(15):
                    base = HEURES_POIDS_DRIFT[heure] * niveau_base_ligne
                    bruit = random.uniform(-3, 3)
                    nb_passagers = max(0, round(base * 3 + bruit))
                    writer.writerow([ligne, heure, nb_passagers])
    print(f"[OK] {chemin} généré (distribution horaire décalée).")


def main():
    generer_dataset_drift()

    mlflow.set_tracking_uri("http://localhost:5000")
    modele = mlflow.sklearn.load_model("models:/anfa-prediction-affluence/Production")

    # Erreur sur les données d'ORIGINE (celles ayant servi à l'entraînement)
    df_origine = pd.read_csv("dataset_affluence.csv")
    pred_origine = modele.predict(df_origine[["ligne_id", "heure"]])
    mae_origine = mean_absolute_error(df_origine["nb_passagers"], pred_origine)
    r2_origine = r2_score(df_origine["nb_passagers"], pred_origine)

    # Erreur sur les données DÉRIVÉES (nouvelle distribution horaire)
    df_drift = pd.read_csv("dataset_affluence_drift.csv")
    pred_drift = modele.predict(df_drift[["ligne_id", "heure"]])
    mae_drift = mean_absolute_error(df_drift["nb_passagers"], pred_drift)
    r2_drift = r2_score(df_drift["nb_passagers"], pred_drift)

    print()
    print("=== Modèle en Production — comparaison origine vs drift ===")
    print(f"Données d'origine : MAE={mae_origine:.2f}  R2={r2_origine:.3f}")
    print(f"Données dérivées  : MAE={mae_drift:.2f}  R2={r2_drift:.3f}")
    print()
    print("[OK] Script terminé SANS ERREUR : le modèle a répondu à chaque")
    print("     requête, y compris quand il se trompait largement.")


if __name__ == "__main__":
    main()
