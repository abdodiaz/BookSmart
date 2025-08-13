import pandas as pd
import numpy as np
from fastapi import FastAPI

from backend.utils import clean_all
from backend.scraping.scrap_books_toscrape import BooksToScraper
from backend.recommender.recommender import modele_recommandation

from backend.database import engine, Base
from backend import models
from backend.routes import users  # Import du routeur users

# Faire une instance de BooksToScraper et lancer le scraping
booktoscrape=BooksToScraper(driver_path=r'C:\Users\lenovo\Documents\BookSmart\backend\chromedriver.exe',headless=True)
df=booktoscrape.scrape_books()
print("Scraping terminé. Nombre de livres récupérés :", len(df))

# Recuperer les données dans un fichier CSV
df.to_csv(r'C:\Users\lenovo\Documents\BookSmart\data\livres_bruts.csv', index=False)

# Nettoyage des données
df_cleaned = clean_all(df)
df_cleaned.to_csv(r'C:\Users\lenovo\Documents\BookSmart\data\livres_nettoyes.csv', index=False)  # Save the cleaned DataFrame to a CSV file

#chargement des modèles de recommandation
modele_recommandation(df_cleaned)

# Création de l'application FastAPI
app = FastAPI()

# Création de la base de données et des tables
Base.metadata.create_all(bind=engine)


# Enregistrement des données nettoyées dans la base de données
df_cleaned.to_sql('livres', con=engine, if_exists='replace', index=False)

# Inclusion du routeur des utilisateurs
app.include_router(users.router)

# Route de test pour vérifier que l'API fonctionne
@app.get("/")
async def root():
    return {"message": "API BookSmart fonctionne !"}
