import pandas as pd
import pickle
from sklearn.preprocessing import OneHotEncoder

print("🔧 RECRÉATION DE L'ENCODEUR À PARTIR DU NOTEBOOK")
print("="*60)

# 1. Charger store_cleaned.csv
try:
    store_df = pd.read_csv('./data/store_cleaned.csv')
    print(f"✅ store_cleaned.csv chargé: {len(store_df)} lignes")
    print(f"Colonnes disponibles: {list(store_df.columns)}")
except FileNotFoundError:
    print("❌ Fichier store_cleaned.csv non trouvé dans ./data/")
    print("Recherche dans le répertoire courant...")
    store_df = pd.read_csv('store_cleaned.csv')
    print(f"✅ store_cleaned.csv chargé depuis le répertoire courant")

# 2. Vérifier les colonnes nécessaires
required_cols = ['StoreType', 'Assortment']
missing_cols = [col for col in required_cols if col not in store_df.columns]
if missing_cols:
    print(f"❌ Colonnes manquantes: {missing_cols}")
    print("Colonnes disponibles:", list(store_df.columns))
    exit(1)

# 3. Afficher les valeurs uniques
print("\n📊 Valeurs uniques dans les données:")
print(f"StoreType: {store_df['StoreType'].unique()}")
print(f"Assortment: {store_df['Assortment'].unique()}")

# 4. Créer l'encodeur EXACTEMENT comme dans le notebook
print("\n🔄 Création de l'encodeur...")
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

# 5. Entraîner l'encodeur
encoder.fit(store_df[['StoreType', 'Assortment']])
print("✅ Encodeur entraîné avec succès!")

# 6. Afficher les catégories apprises
print(f"\nCatégories StoreType apprises: {encoder.categories_[0]}")
print(f"Catégories Assortment apprises: {encoder.categories_[1]}")

# 7. Tester l'encodeur
print("\n🔄 Test de l'encodeur...")
test_data = pd.DataFrame({
    'StoreType': ['a', 'b', 'c', 'd'],
    'Assortment': ['a', 'b', 'c', 'a']
})
try:
    encoded_test = encoder.transform(test_data[['StoreType', 'Assortment']])
    feature_names = encoder.get_feature_names_out(['StoreType', 'Assortment'])
    print(f"✅ Test réussi! Shape encodée: {encoded_test.shape}")
    print(f"Features générées: {feature_names}")
    
    # Afficher un exemple
    print("\nExemple d'encodage:")
    for i, (_, row) in enumerate(test_data.iterrows()):
        print(f"  {row['StoreType']},{row['Assortment']} -> {encoded_test[i]}")
        
except Exception as e:
    print(f"❌ Erreur test: {e}")

# 8. Sauvegarder l'encodeur
print("\n💾 Sauvegarde de l'encodeur...")
output_file = './models/encoder_recreated.pkl'
with open(output_file, 'wb') as f:
    pickle.dump(encoder, f)
print(f"✅ Encodeur sauvegardé dans: {output_file}")

# 9. Vérifier que l'encodeur peut être rechargé
print("\n🔄 Vérification du rechargement...")
with open(output_file, 'rb') as f:
    encoder_loaded = pickle.load(f)
print("✅ Encodeur rechargé avec succès!")

# 10. Comparer les versions
print("\n📦 Versions des bibliothèques utilisées:")
import sklearn
import numpy as np
print(f"Scikit-learn: {sklearn.__version__}")
print(f"NumPy: {np.__version__}")

print("\n" + "="*60)
print("🎉 ENCODEUR PRÊT À L'EMPLOI!")
print(f"Utilisez maintenant: {output_file}")