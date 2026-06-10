# PropPredict — Outil intelligent d'estimation immobilière par Intelligence Artificielle

> **PropPredict** est une application web intuitive dotée d'une carte interactive qui permet d'obtenir l'estimation financière ultra-précise d'un bien immobilier en quelques secondes. En combinant la puissance de l'Intelligence Artificielle et des données foncières officielles, l'utilisateur a juste à saisir une adresse ou cliquer sur la carte pour évaluer la valeur de son bien.

---

## 🛠️ Fiche Technique & Mots-Clés (Pour les profils Tech)

* **Architecture Globale** : `PropPredict — Pipeline XGBoost & Interface Flask pour l'Estimation Immobilière`
* **Data Science & ML** : `XGBoost Regressor`, `Scikit-Learn Pipeline`, `Pandas`, `Joblib`, Feature Engineering avancé (`surface_par_piece`, géolocalisation).
* **Développement Web / Backend** : `Flask (Python)`, `Requests` (Proxy API REST anti-CORS).
* **Interface & UX (Frontend)** : `JavaScript (Vanilla ES6)`, `Leaflet.js` (Cartographie interactive), `CSS3 Variables` (Design épuré et responsive), Autocomplétion d'adresse dynamique avec anti-rebond (*debounce*), Gestion d'historique persistant (`localStorage`).

---

## 🚀 Fonctionnalités Clés

* **Modèle Prédictif de Pointe** : Pipeline d'estimation basé sur l'algorithme de gradient boosting **XGBoost**, entraîné sur les données officielles de l'État français (DVF - Demandes de Valeurs Foncières).
* **Feature Engineering Temps Réel** : Prise en compte de variables calculées à la volée (coordonnées GPS de haute précision, ratios de surface, saisonnalité automatisée).
* **Ergonomie Épurée** : Suppression des frictions utilisateurs (pas de choix de dates fastidieux), affichage immédiat de la valeur totale et du prix moyen au m².
* **Proxy de Géocodage Intégré** : Recherche d'adresse prédictive fluide connectée de manière sécurisée à l'API Nominatim d'OpenStreetMap.
* **Sauvegarde Locale** : Mémorisation automatique des 10 dernières estimations directement dans le navigateur pour une consultation instantanée et hors-ligne.

---

## 📂 Structure du Projet

```text
prediction-immobilier/
│
├── app.py                   # Serveur web Flask (Backend, Routage & Proxy API)
├── requirements.txt         # Dépendances Python du projet
├── .gitignore               # Fichiers exclus du suivi de version
├── README.md                # Documentation du projet
│
├── models/
│   └── pipeline_final_pro.pkl  # Pipeline de Machine Learning entraîné et sauvegardé
│
├── src/
│   └── models/
│       └── train_france_pipeline.py  # Script d'origine ayant servi à l'entraînement
│
├── static/                  # Assets Frontend
│   ├── app.js               # Logique JS (Carte, Autocomplétion, LocalStorage)
│   └── style.css            # Habillage graphique UI/UX moderne
│
└── templates/
    └── index.html           # Interface utilisateur unique (Single Page App)