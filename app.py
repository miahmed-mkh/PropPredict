#!/usr/bin/env python3
from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

DEPARTEMENTS = {
    '01': 'Ain', '02': 'Aisne', '03': 'Allier', '04': 'Alpes-de-Haute-Provence',
    '05': 'Hautes-Alpes', '06': 'Alpes-Maritimes', '07': 'Ardèche', '08': 'Ardennes',
    '09': 'Ariège', '10': 'Aube', '11': 'Aude', '12': 'Aveyron', '13': 'Bouches-du-Rhône',
    '14': 'Calvados', '15': 'Cantal', '16': 'Charente', '17': 'Charente-Maritime',
    '18': 'Cher', '19': 'Corrèze', '21': "Côte-d'Or", '22': "Côtes-d'Armor",
    '23': 'Creuse', '24': 'Dordogne', '25': 'Doubs', '26': 'Drôme', '27': 'Eure',
    '28': 'Eure-et-Loir', '29': 'Finistère', '2A': 'Corse-du-Sud', '2B': 'Haute-Corse',
    '30': 'Gard', '31': 'Haute-Garonne', '32': 'Gers', '33': 'Gironde',
    '34': 'Hérault', '35': 'Ille-et-Vilaine', '36': 'Indre', '37': 'Indre-et-Loire',
    '38': 'Isère', '39': 'Jura', '40': 'Landes', '41': 'Loir-et-Cher',
    '42': 'Loire', '43': 'Haute-Loire', '44': 'Loire-Atlantique', '45': 'Loiret',
    '46': 'Lot', '47': 'Lot-et-Garonne', '48': 'Lozère', '49': 'Maine-et-Loire',
    '50': 'Manche', '51': 'Marne', '52': 'Haute-Marne', '53': 'Mayenne',
    '54': 'Meurthe-et-Moselle', '55': 'Meuse', '56': 'Morbihan', '57': 'Moselle',
    '58': 'Nièvre', '59': 'Nord', '60': 'Oise', '61': 'Orne', '62': 'Pas-de-Calais',
    '63': 'Puy-de-Dôme', '64': 'Pyrénées-Atlantiques', '65': 'Hautes-Pyrénées',
    '66': 'Pyrénées-Orientales', '67': 'Bas-Rhin', '68': 'Haut-Rhin', '69': 'Rhône',
    '70': 'Haute-Saône', '71': 'Saône-et-Loire', '72': 'Sarthe', '73': 'Savoie',
    '74': 'Haute-Savoie', '75': 'Paris', '76': 'Seine-Maritime', '77': 'Seine-et-Marne',
    '78': 'Yvelines', '79': 'Deux-Sèvres', '80': 'Somme', '81': 'Tarn',
    '82': 'Tarn-et-Garonne', '83': 'Var', '84': 'Vaucluse', '85': 'Vendée',
    '86': 'Vienne', '87': 'Haute-Vienne', '88': 'Vosges', '89': 'Yonne',
    '90': 'Territoire de Belfort', '91': 'Essonne', '92': 'Hauts-de-Seine',
    '93': 'Seine-Saint-Denis', '94': 'Val-de-Marne', '95': "Val-d'Oise",
    '971': 'Guadeloupe', '972': 'Martinique', '973': 'Guyane',
    '974': 'La Réunion', '976': 'Mayotte'
}

print("Chargement du pipeline...")
try:
    pipeline = joblib.load("models/pipeline_dvf_pro.pkl")
    print("Pipeline chargé avec succès.")
except Exception as e:
    print(f"Erreur chargement pipeline: {e}")
    pipeline = None


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None
    form_data = {}

    if request.method == "POST":
        try:
            form_data = request.form.to_dict()

            surface_raw = form_data.get("surface_reelle_bati", "").strip()
            pieces_raw = form_data.get("nombre_pieces_principales", "").strip()
            type_local = form_data.get("type_local", "").strip()

            code_postal = form_data.get("code_postal", "").strip()
            ville = form_data.get("ville", "").strip()
            adresse = form_data.get("adresse", "").strip()

            code_departement = form_data.get("code_departement", "").strip()
            latitude_raw = form_data.get("latitude", "").strip()
            longitude_raw = form_data.get("longitude", "").strip()

            annee_raw = form_data.get("annee_mutation", "2026").strip()
            mois_raw = form_data.get("mois_mutation", "5").strip()

            if not surface_raw or not pieces_raw:
                raise ValueError("Veuillez renseigner la surface et le nombre de pièces.")

            if not type_local:
                raise ValueError("Veuillez sélectionner le type de bien.")

            if not latitude_raw or not longitude_raw:
                raise ValueError("Veuillez choisir une adresse suggérée ou sélectionner un point sur la carte.")

            if not code_departement:
                raise ValueError("Le département n'a pas été déterminé automatiquement.")

            if pipeline is None:
                raise ValueError("Le pipeline de prédiction n'est pas chargé.")

            surface = float(surface_raw)
            pieces = float(pieces_raw)
            latitude = float(latitude_raw)
            longitude = float(longitude_raw)
            annee = int(annee_raw)
            mois = int(mois_raw)

            if surface <= 0:
                raise ValueError("La surface doit être supérieure à 0.")
            if pieces <= 0:
                raise ValueError("Le nombre de pièces doit être supérieur à 0.")

            input_df = pd.DataFrame([{
                "surface_reelle_bati": surface,
                "nombre_pieces_principales": pieces,
                "type_local": type_local,
                "code_departement": code_departement,
                "longitude": longitude,
                "latitude": latitude,
                "annee": annee,
                "mois": mois
            }])

            prix_m2 = float(pipeline.predict(input_df)[0])

            prediction = {
                "prix_m2": prix_m2,
                "prix_total": prix_m2 * surface,
                "fourchette_basse": prix_m2 * surface * 0.9,
                "fourchette_haute": prix_m2 * surface * 1.1,
                "surface": surface,
                "pieces": pieces,
                "type_local": type_local,
                "code_postal": code_postal,
                "ville": ville,
                "adresse": adresse,
                "departement": code_departement,
                "departement_nom": DEPARTEMENTS.get(code_departement, code_departement),
                "latitude": latitude,
                "longitude": longitude
            }

        except ValueError as ve:
            error = str(ve)
        except Exception as e:
            error = f"Erreur lors de l'estimation : {str(e)}"

    return render_template(
        "index.html",
        departements=DEPARTEMENTS,
        prediction=prediction,
        error=error,
        form_data=form_data,
        annee_courante=2026,
        mois_courant=5,
    )


if __name__ == "__main__":
    app.run(debug=True)