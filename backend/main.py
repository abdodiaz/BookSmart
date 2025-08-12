import pandas as pd
import numpy as np
from utils import clean_all

df=pd.read_csv(r'C:\Users\lenovo\Documents\BookSmart\data\livres_bruts.csv')
print(df.head())

df_cleaned = clean_all(df)
df_cleaned.to_csv(r'C:\Users\lenovo\Documents\BookSmart\data\livres_nettoyes.csv', index=False)  # Save the cleaned DataFrame to a CSV file