# PropPredict — Outil intelligent d'estimation immobilière par Intelligence Artificielle

> **PropPredict** est une application web intuitive dotée d'une carte interactive qui permet d'obtenir l'estimation financière ultra-précise d'un bien immobilier en quelques secondes. En combinant la puissance de l'Intelligence Artificielle et des données foncières officielles, l'utilisateur a juste à saisir une adresse ou cliquer sur la carte pour évaluer la valeur de son bien.

---

## Contexte, Problématique & Approche ML

Le secteur immobilier français constitue un pilier économique majeur, générant annuellement **1,3 trillion d'euros** à travers environ un million de transactions. Malgré cette dynamique, les acteurs du marché, qu'ils soient acheteurs ou vendeurs, se heurtent à une absence d'outils transparents pour évaluer la valeur des biens en temps réel. Les solutions actuelles, portées par des plateformes comme MeilleursAgents ou PAP, présentent souvent des méthodologies opaques et des coûts d'accès élevés qui limitent leur accessibilité. 

Dans ce contexte, l'ouverture des données des **Demandes de Valeurs Foncières (DVF)** par la DGFiP représente une opportunité majeure, mettant à disposition un ensemble de **2,3 millions de transactions réelles** enregistrées entre 2014 et 2025. Le présent projet s'inscrit dans cette démarche d'ouverture en exploitant ce jeu de données massif pour concevoir un estimateur performant et libre de droit.

La problématique de ce projet réside dans les limites intrinsèques des outils propriétaires actuels, dont les algorithmes demeurent secrets et les estimations se cantonnent souvent à des moyennes communales trop imprécises. L'absence de géolocalisation fine et le manque d'interfaces web accessibles au grand public constitueraient des freins à une estimation immobilière démocratisée si les travaux se limitaient à de simples scripts techniques. 

Le problème d'estimation des prix immobiliers est traité comme une **régression supervisée classique** où les caractéristiques d'un bien (surface, localisation, type, temporalité) servent à prédire sa valeur au mètre carré. Le pipeline complet respecte scrupuleusement les étapes du cycle de vie standard d'un projet d'apprentissage automatique : collecte et exploration préliminaire des données (EDA), prétraitement intensif et ingénierie des caractéristiques, sélection et entraînement de plusieurs modèles candidats, évaluation rigoureuse sur un jeu de test indépendant, puis déploiement opérationnel via une API Flask accessible par interface web. Cette démarche méthodique garantit la reproductibilité des résultats et la robustesse du système final face à des données réelles hétérogènes.

---

## Architecture du Système

L'application adopte une **architecture web client-serveur classique** structurée en trois couches interdépendantes :

1. **La couche présentation (Frontend HTML/JavaScript)** : Collecte les entrées utilisateur de manière fluide (carte, formulaire) et affiche les prédictions sous forme interactive.
2. **La couche métier (Backend Flask)** : Orchestre les requêtes, l'appel à l'API de géocodage, la construction dynamique du DataFrame d'inférence et l'exécution du pipeline de prédiction.
3. **La couche données** : Combine le modèle persistant (`.pkl`), l'API publique française de géocodage et les métadonnées statiques des départements.

Cette séparation stricte des responsabilités garantit la maintenabilité, la testabilité et l'évolutivité du système.

---

## Objectifs & Évaluation des Performances

L’évaluation du modèle constitue une étape essentielle pour vérifier sa capacité à fournir des estimations fiables dans un contexte réel. Dans ce projet, la performance du système a été mesurée sur un jeu de test indépendant, distinct des données utilisées pour l’entraînement, conformément aux bonnes pratiques de l’apprentissage supervisé. Cette séparation entre apprentissage et évaluation permet de mesurer la capacité de généralisation du modèle et de limiter le risque de surapprentissage. 

Le projet s’inscrit dans une démarche de machine learning appliquée à des données réelles, avec comparaison de modèles, justification du choix final et intégration d’une interface de test, ce qui correspond aux attendus académiques et industriels d’un projet ML complet.

L'objectif central de validation statistique est d'atteindre :
* Un coefficient de détermination **$R^2 > 0,75$**
* Une erreur absolue moyenne en pourcentage **$\text{MAPE} < 20\%$**

---

## Fiche Technique & Mots-Clés

* **Architecture Globale** : `PropPredict — Pipeline XGBoost & Interface Flask pour l'Estimation Immobilière`
* **Data Science & ML** : `XGBoost Regressor`, `Scikit-Learn Pipeline`, `Pandas`, `Joblib`, Feature Engineering (`surface_par_piece`, coordonnées géographiques).
* **Développement Web / Backend** : `Flask (Python)`, `Requests` (Proxy API REST anti-CORS).
* **Interface & UX (Frontend)** : `JavaScript (Vanilla ES6)`, `Leaflet.js` (Cartographie interactive), `CSS3 Variables`, Autocomplétion d'adresse dynamique avec anti-rebond (*debounce*), Gestion d'historique persistant (`localStorage`).
* **DevOps & Pérennisation** : Architecture prête pour un déploiement sous `Docker`.

---

## Le Jeu de Données (DVF) & Préparation

Le dataset **Demandes de Valeurs Foncières (DVF)** est une publication officielle de la Direction Générale des Finances Publiques (DGFiP), disponible sur data.gouv.fr. Il recense l'intégralité des transactions immobilières notariées en France métropolitaine depuis 2014.

### Chiffres clés du Pipeline Data :
* **Dataset final** : **1 812 456 transactions propres** (soit une réduction de 23% par rapport au dataset brut après nettoyage et traitement des valeurs aberrantes).
* **Variables** : **8 variables explicatives** sélectionnées et la variable cible `prix_m²`.
* **Partition Train/Test** : Ratio **80/20**, représentant **1,45 million d'observations d'entraînement** et **362 000 observations de test**.
* **Validation post-nettoyage** : 
  * Absence totale de valeurs manquantes résiduelles.
  * Réduction de l'asymétrie (*skewness*) de la distribution du `prix_m²` de **2,1 à 1,2**.
  * Corrélation maximale de **0,45** entre les *features* et la cible.

---

## Fonctionnalités Applicatives Avancées

* **Inférence via Pipeline Scikit-learn** : Le fichier de production `pipeline_final_pro.pkl` encapsule l'intégralité du traitement (nettoyage, typage automatique des variables en `category` et prédiction via le régresseur **XGBoost**).
* **Feature Engineering Temps Réel** : Isolation des coordonnées géographiques et calcul automatique de la compacité du logement (`surface_par_piece`) à la volée.
* **Système d'Autocomplétion d'Adresses** : Recherche prédictive fluide s'appuyant sur l'API de la **Base Adresse Nationale (BAN)** et Nominatim OpenStreetMap.
* **Visualisation Cartographique Interactive** : Sélection de l'emplacement et ajustement des coordonnées par glisser-déposer de marqueur via **Leaflet**.
* **Sauvegarde Locale** : Mémorisation automatique des 10 dernières estimations directement dans le navigateur via le `localStorage` pour une consultation instantanée hors-ligne.

---

## Structure du Projet

```text
PropPredict/
│
├── app.py                   # Serveur web Flask (Backend, Routage & Proxy API)
├── requirements.txt         # Dépendances Python du projet
├── README.md                # Documentation du projet
│
├── models/
│   └── pipeline_final_pro.pkl  # Pipeline de Machine Learning entraîné et sauvegardé
│
│
├── static/                  # Assets Frontend
│   ├── app.js               # Logique JS (Carte, Autocomplétion, LocalStorage)
│   └── style.css            # Habillage graphique UI/UX moderne
│
└── templates/
    └── index.html           # Interface utilisateur unique (Single Page App)