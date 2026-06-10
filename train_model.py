# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import joblib
from pathlib import Path

csv_path = Path("data/processed/dvf_france_pro.csv")
print(f"Loading: {csv_path}")

df = pd.read_csv(
    csv_path,
    low_memory=False,
    dtype={
        "code_departement": "string",
        "type_local": "string"
    }
)

# Supprime les colonnes dupliquees comme longitude/latitude si elles existent 2 fois
df = df.loc[:, ~df.columns.duplicated()].copy()

# Force les colonnes categorielles en texte
df["code_departement"] = df["code_departement"].astype("string").str.strip()
df["type_local"] = df["type_local"].astype("string").str.strip()

# Force les colonnes numeriques
num_cols = [
    "surface_reelle_bati",
    "nombre_pieces_principales",
    "longitude",
    "latitude",
    "prix_m2",
    "annee",
    "mois",
]

for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print(f"Initial shape: {df.shape}")
print("Columns:", df.columns.tolist())
print(df.dtypes)

# Supprime les lignes avec valeurs manquantes sur les colonnes utiles
df = df.dropna(subset=[
    "surface_reelle_bati",
    "nombre_pieces_principales",
    "type_local",
    "code_departement",
    "longitude",
    "latitude",
    "prix_m2",
    "annee",
    "mois",
])

df = df.dropna(subset=["prix_m2"])
df = df[(df["prix_m2"] > 500) & (df["prix_m2"] < 50000)]
df["surface_reelle_bati"] = df["surface_reelle_bati"].clip(lower=10, upper=500)
df["nombre_pieces_principales"] = df["nombre_pieces_principales"].clip(lower=1, upper=15)

features = [
    "surface_reelle_bati",
    "nombre_pieces_principales",
    "type_local",
    "code_departement",
    "longitude",
    "latitude",
    "annee",
    "mois",
]

X = df[features]
y = df["prix_m2"]

numeric_features = [
    "surface_reelle_bati",
    "nombre_pieces_principales",
    "longitude",
    "latitude",
    "annee",
    "mois",
]

categorical_features = [
    "type_local",
    "code_departement",
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]),
            numeric_features,
        ),
        (
            "cat",
            Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("ohe", OneHotEncoder(handle_unknown="ignore")),
            ]),
            categorical_features,
        ),
    ]
)

pipeline = Pipeline([
    ("preproc", preprocessor),
    ("model", RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
        max_depth=15
    )),
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

pipeline.fit(X_train, y_train)

train_r2 = pipeline.score(X_train, y_train)
test_r2 = pipeline.score(X_test, y_test)
y_pred = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred) * 100

print("Train R2:", round(train_r2, 3))
print("Test R2:", round(test_r2, 3))
print("Test MAE:", round(mae, 0), "EUR/m2")
print("Test MAPE:", round(mape, 1), "%")

cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring="r2")
print("CV R2:", round(cv_scores.mean(), 3), "+/-", round(cv_scores.std(), 3))

Path("models").mkdir(exist_ok=True)
joblib.dump(pipeline, "models/pipeline_dvf_pro.pkl")
print("Saved: models/pipeline_dvf_pro.pkl")