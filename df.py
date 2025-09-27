import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from joblib import Parallel, delayed

# Charger les données JSON et séparer target et query
def load_data(json_file):
    with open(json_file, "r") as infile:
        data = json.load(infile)

    target_data = []
    query_data = []

    for chunk_result in data:
        for chunk_id, sequences in chunk_result.items():
            target_text = " ".join(sequences["target"])
            query_text = " ".join(sequences["query"])

            target_data.append({"chunk": chunk_id, "text": target_text, "type": "target"})
            query_data.append({"chunk": chunk_id, "text": query_text, "type": "query"})

    return pd.DataFrame(target_data), pd.DataFrame(query_data)

# Charger les données
json_file = "exons_resultats.json"
target_df, query_df = load_data(json_file)

# Ajouter des étiquettes (deux espèces : Espèce_1 et Espèce_2)
import random
species_labels = ["canis_lupus", "feluis_catus"]

# Simuler des étiquettes pour chaque type (à remplacer par tes vraies données)
target_df["label"] = [species_labels[0] for _ in range(len(target_df))]
query_df["label"] = [species_labels[1] for _ in range(len(query_df))]

# Vérifier les premières lignes
print("Target DataFrame:")
print(target_df.head())
print("\nQuery DataFrame:")
print(query_df.head())

target_df.to_csv('target.csv')
query_df.to_csv('query.csv')



# # Fonction pour entraîner le modèle et obtenir le rapport de classification
# def train_classification_model(df, exon_type):
#     print(f"\nEntraînement du modèle pour les exons '{exon_type}':\n")

#     # Séparer les données en entrées (X) et étiquettes (y)
#     X = df["text"]
#     y = df["label"]

#     # Division en jeu d'entraînement et de test
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     # Vectorisation avec TF-IDF
#     vectorizer = TfidfVectorizer()
#     X_train_tfidf = vectorizer.fit_transform(X_train)
#     X_test_tfidf = vectorizer.transform(X_test)

#     # Entraînement du modèle Logistic Regression
#     model = LogisticRegression(max_iter=1000)
#     model.fit(X_train_tfidf, y_train)

#     # Prédiction et évaluation
#     y_pred = model.predict(X_test_tfidf)
#     print("Rapport de classification :")
#     print(classification_report(y_test, y_pred))

#     return model, vectorizer

# # Parallélisation des tâches d'entraînement des modèles pour 'target' et 'query'
# models = Parallel(n_jobs=2)(delayed(train_classification_model)(df, exon_type)
#                              for df, exon_type in [(target_df, "target"), (query_df, "query")])

# # Récupérer les modèles et les vectoriseurs
# target_model, target_vectorizer = models[0]
# query_model, query_vectorizer = models[1]

# # Exemple de nouvelles séquences d'exons
# new_target_exons = ["GTGCCCGAGACTCGCGTGGC", "TGTATGCTGAAACTTCT"]
# new_query_exons = ["GAGGGAACGGGCCTCT", "TCCAACTCTACTTTGGAATTGT"]

# # Prédire avec le modèle pour 'target'
# new_target_tfidf = target_vectorizer.transform(new_target_exons)
# target_predictions = target_model.predict(new_target_tfidf)
# print("\nPrédictions pour les nouvelles séquences 'target':")
# for exon, pred in zip(new_target_exons, target_predictions):
#     print(f"Exon: {exon} --> Espèce prédite: {pred}")

# # Prédire avec le modèle pour 'query'
# new_query_tfidf = query_vectorizer.transform(new_query_exons)
# query_predictions = query_model.predict(new_query_tfidf)
# print("\nPrédictions pour les nouvelles séquences 'query':")
# for exon, pred in zip(new_query_exons, query_predictions):
#     print(f"Exon: {exon} --> Espèce prédite: {pred}")