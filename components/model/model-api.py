from flask import Flask, jsonify, request
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

# Récupération des données de la base MongoDB
data = pd.DataFrame(list(collection.find()))

# Suppression des lignes avec des valeurs manquantes
data = data.dropna(subset=['category', 'brand', 'rating', 'description'])

app = Flask(__name__)

# API endpoint for product recommendations
@app.route('/recommend', methods=['GET'])
def recommend():
    search_query = request.args.get('search')
    if not search_query:
        return jsonify({'error': 'Please provide a search term in the URL parameter `search`.'}), 400
    
    matching_products = data[data['name'].str.contains(search_query, case=False, na=False)]
    
    if not matching_products.empty:
        idx = matching_products.index[0]
        similar_products_indices = np.argsort(similarity_vectors[idx])[::-1][1:6]
        similar_products = data.iloc[similar_products_indices][['name', 'category', 'price', 'rating']].to_dict(orient='records')
        return jsonify(similar_products)
    else:
        return jsonify({'message': 'No products found in the database matching your search. Please try with other terms.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
