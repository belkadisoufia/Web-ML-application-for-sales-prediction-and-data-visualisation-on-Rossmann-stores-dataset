from flask import Flask, request, render_template, send_file, jsonify, redirect, url_for
import pickle
import pandas as pd
import numpy as np
import os
from helper import get_total_sales, store_data, easter_data

# Chargement global
print("Chargement des fichiers...")
try:
    store_df = store_data()
    easter_df = easter_data()
    
    with open('./models/ml_model.pkl', 'rb') as f:
        ml_model = pickle.load(f)
    
    try:
        encoder = pickle.load(open('./models/encoder_recreated.pkl', 'rb'))
      
    except:
        encoder = pickle.load(open('./models/encoder.pkl', 'rb'))
    
    print("✅ Fichiers chargés avec succès !")
    
except Exception as e:
    print(f"❌ ERREUR AU CHARGEMENT : {e}")
    raise e

application = Flask(__name__)

# Route par défaut - Page d'accueil (landing)
@application.route('/')
def landing():
    return render_template('landing.html')

# Route pour la page de prédiction
@application.route('/predict')
def predict():
    return render_template('index.html', total="", average="")

# Route pour la page dashboard
@application.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Route pour le dashboard live
@application.route('/dashboard_live')
def dashboard_live():
    return render_template('dashboard_live.html')

# Route pour télécharger le dashboard
@application.route('/download_dashboard')
def download_dashboard():
    try:
        dashboard_path = './dashboard/Dashboard_Rossmann.pbix'
        if os.path.exists(dashboard_path):
            return send_file(
                dashboard_path,
                as_attachment=True,
                download_name='Dashboard_Rossmann.pbix',
                mimetype='application/octet-stream'
            )
        else:
            print("Fichier non trouvé")
            return redirect(url_for('dashboard'))
    except Exception as e:
        print(f"Erreur: {e}")
        return redirect(url_for('dashboard'))

@application.route('/predict_api', methods=['POST'])
def predict_api():
    try:
        data = list(request.form.values())
        print(f"Données reçues: {data}")
        
        if len(data) < 3:
            return render_template('index.html', 
                                   total="Erreur: Données incomplètes", 
                                   average="")
        
        store_id, start_date, end_date = int(data[0]), data[1], data[2]
        
        print(f"Prédiction: Store={store_id}, De={start_date} à={end_date}")

        results = get_total_sales(store_id, start_date, end_date, store_df, easter_df, ml_model, encoder)
        
        sales_list = list(results.values())
        total = sum(sales_list)
        avg = total / len(sales_list)
        
        print(f"Résultat: Total={total}, Moyenne={avg}")

        return render_template('index.html', 
                               total=f"$ {round(total, 2)}", 
                               average=f"$ {round(avg, 2)}")
                               
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return render_template('index.html', 
                               total=f"Erreur: {str(e)[:50]}", 
                               average="")

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)