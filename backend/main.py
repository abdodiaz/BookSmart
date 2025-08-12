from fastapi import FastAPI
from backend.database import Base, engine
from backend import models

# Création des tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BookSmart API")

@app.get("/")
def root():
    return {"message": "Bienvenue dans l'API BookSmart"}