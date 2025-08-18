import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from backend import crud

class Recommender:
    def __init__(self, db: Session):
        self.db = db
        self.livres = self.load_livres()
        self.vectorizer = None
        self.tfidf_matrix = None
        self.load_or_train_model()

    def load_livres(self):
        livres = crud.get_all_livres(self.db)
        data = []
        for livre in livres:
            data.append({
                "id": livre.id,
                "titre": livre.titre,
                "description": livre.description or livre.titre
            })
        return pd.DataFrame(data)

    def load_or_train_model(self):
        try:
            self.vectorizer = joblib.load(r'backend/recommender/tfidf_vectorizer.joblib')
            self.tfidf_matrix = joblib.load(r'backend/recommender/cosine_similarity_matrix.joblib')
        except FileNotFoundError:
            self.train_model()

    def train_model(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.livres['description'])
        joblib.dump(self.vectorizer, r'backend/recommender/tfidf_vectorizer.joblib')
        joblib.dump(self.tfidf_matrix, r'backend/recommender/cosine_similarity_matrix.joblib')
        print("Modèle et matrice sauvegardés avec succès.")

    def get_recommendations(self, description, top_n=5):
        desc_vec = self.vectorizer.transform([description])
        cosine_sim = cosine_similarity(desc_vec, self.tfidf_matrix).flatten()
        top_indices = cosine_sim.argsort()[-top_n:][::-1]
        return self.livres.iloc[top_indices].to_dict(orient='records')
