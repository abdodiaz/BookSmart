import pandas as pd
import numpy as np
from utils import clean_all
from fastapi import FastAPI

from scraping.scrap_books_toscrape import BooksToScraper
from recommender.recommender import modele_recommandation

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
