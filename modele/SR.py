# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 13:14:12 2024

@author: NOREYNI
"""

import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['test']
collection = db['products']

# Récupération des données de la base MongoDB
data = pd.DataFrame(list(collection.find()))

# Suppression des lignes avec des valeurs manquantes
data = data.dropna(subset=['category', 'brand', 'rating', 'description'])

# Fonction d'encodage binaire
def binary_encoding(column):
    unique_items = pd.unique(np.array([item for sublist in column for item in re.split(r', \s*', sublist)]))
    binary = pd.DataFrame(0, index=column.index, columns=unique_items)
    
    for idx, row in enumerate(column):
        for item in re.split(r', \s*', row):
            binary.at[idx, item] = 1
            
    return binary

# Encodage binaire pour les catégories
binary_categories = binary_encoding(data['category'])

# Encodage binaire pour les marques
binary_brands = binary_encoding(data['brand'])

# Encodage binaire pour les ratings
binary_ratings = pd.get_dummies(data['rating'])

# Encodage binaire pour les descriptions
def binary_description(column):
    words = []

    for text in column:
        text_tokens = word_tokenize(text)
        tokens_without_sw = [word.lower() for word in text_tokens if not word in stopwords.words()]
        words.append(tokens_without_sw)

    words = [item for sublist in words for item in sublist]
    words_list = sorted(set(words))
    
    binary = pd.DataFrame(0, index=column.index, columns=words_list)
    
    for idx, row in enumerate(column):
        for word in word_tokenize(row):
            if word.lower() in words_list:
                binary.at[idx, word.lower()] = 1
                
    return binary

binary_words = binary_description(data['description'])

# Création du DataFrame binaire final pour les produits
binary_products = pd.concat([binary_categories, binary_brands, binary_ratings, binary_words], axis=1)

# Développement du moteur de recommandation
def recommender(search):
    if search in data['name'].values:
        idx = data[data['name'] == search].index[0]
        
        point1 = np.array(binary_products.iloc[idx]).reshape(1, -1).astype(float)
        
        norm_point1 = np.linalg.norm(point1)
        norm_binary_products = np.linalg.norm(binary_products.values.astype(float), axis=1)
        
        cos_sim = np.dot(binary_products.values.astype(float), point1.T).flatten() / (norm_binary_products * norm_point1)
        
        data_copy = data.copy()
        data_copy['cos_sim'] = cos_sim
        results = data_copy.sort_values('cos_sim', ascending=False)
        results = results[results['name'] != search]
        
        top_results = results.head(5)
        return top_results
    else:
        return "Produit non trouvé dans la base de données. Veuillez vérifier l'orthographe."

# Exemples de recommandations
print(recommender('Free Shirt'))
