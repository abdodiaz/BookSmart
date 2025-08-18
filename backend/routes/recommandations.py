from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import backend.crud
import backend.database
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

router = APIRouter(
    prefix="/api/recommandations",
    tags=["recommandations"]
)

class Recommender:
    def __init__(self, db: Session):
        self.db = db
        self.livres = self.load_livres()
        self.vectorizer = TfidfVectorizer(stop_words='french')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.livres['description'])

    def load_livres(self):
        livres = backend.crud.get_all_livres(self.db)
        data = []
        for l in livres:
            data.append({
                "id": l.id,
                "titre": l.titre,
                "description": l.description or l.titre
            })
        return pd.DataFrame(data)

    def get_recommendations(self, description, top_n=5):
        desc_vec = self.vectorizer.transform([description])
        cosine_sim = cosine_similarity(desc_vec, self.tfidf_matrix).flatten()
        top_indices = cosine_sim.argsort()[-top_n:][::-1]
        return self.livres.iloc[top_indices].to_dict(orient='records')

    def save_model(self, path="model.pkl"):
        joblib.dump((self.vectorizer, self.tfidf_matrix, self.livres), path)

    @staticmethod
    def load_model(path="model.pkl"):
        return joblib.load(path)

@router.post("/")
def recommend(description: str, db: Session = Depends(backend.database.get_db)):
    recommender = Recommender(db)
    return recommender.get_recommendations(description)
