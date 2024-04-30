import json
import pickle
import pandas as pd
import numpy as np
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['next-amazona-v2']
collection = db['products']

# Charger le modèle pré-entraîné
with open('modele_v2.pkl', 'rb') as f:
    similarity_vectors = pickle.load(f)

# Convertir le vecteur de similarité en JSON
similarity_json = similarity_vectors.tolist()

# Écrire le JSON dans un fichier JavaScript
with open('similarite_vectors.js', 'w') as f:
    f.write('const similarityVectors = ')
    json.dump(similarity_json, f)

# Charger le DataFrame 'data'
# (Assurez-vous que le chemin d'accès au fichier est correct)
#data = pd.read_csv('chemin_vers_votre_fichier.csv')  # Remplacez 'chemin_vers_votre_fichier.csv' par le chemin d'accès à votre fichier CSV

# Récupération des données de la base MongoDB
data = pd.DataFrame(list(collection.find()))

# Suppression des lignes avec des valeurs manquantes
data = data.dropna(subset=['category', 'brand', 'rating', 'description'])

# Développement du moteur de recommandation
def recommender(search):
    matching_products = data[data['name'].str.contains(search, case=False, na=False)]
    
    if not matching_products.empty:
        idx = matching_products.index[0]
        similar_products_indices = np.argsort(similarity_vectors[idx])[::-1][1:6]
        
        # Afficher seulement les colonnes 'product_id', 'name' et 'slug'
        return data.iloc[similar_products_indices][['name', 'category','price','rating']]
        #return data.iloc[similar_products_indices]

    else:
        return "Aucun produit trouvé dans la base de données correspondant à votre recherche. Veuillez essayer avec d'autres termes."

# Appel de la fonction recommender
print(recommender('shirt'))
