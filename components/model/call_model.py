import json
import pickle
import pandas as pd
import numpy as np
from pymongo import MongoClient
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
# Connexion à MongoDB

class SearchQuery(BaseModel):
    query: str

client = MongoClient('localhost', 27017)
db = client['test']
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


# Route POST pour la fonction de recommandation
@app.post("/recommender")

# Développement du moteur de recommandation
def recommend_products(query_data: SearchQuery):
    query = query_data.query

    # Développement du moteur de recommandation
    matching_products = data[data['name'].str.contains(query, case=False, na=False)]

    if not matching_products.empty:
        idx = matching_products.index[0]
        similar_products_indices = np.argsort(similarity_vectors[idx])[::-1][1:6]

        # Créer un tableau de produits au format JSON
        recommended_products = []
        for idx in similar_products_indices:
            product = {
                #"_id": data.iloc[idx]['_id'],
               # "slug": data.iloc[idx]['slug'],
                "name": data.iloc[idx]['name'],
                "category": data.iloc[idx]['category'],
                "price": data.iloc[idx]['price'],
                "rating": data.iloc[idx]['rating'],
                "brand": data.iloc[idx]['brand']
            }
            recommended_products.append(product)

        # Renvoyer la réponse au format JSON
        return recommended_products
    else:
        # Si aucun produit correspondant n'est trouvé, renvoyer un tableau vide
        return []

# Appel de la fonction recommender
print(recommend_products(SearchQuery(query='shirt')))