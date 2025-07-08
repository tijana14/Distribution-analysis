import pandas as pd
import numpy as np

df = pd.read_csv('online_store_data.csv')

# Funkcija za konverziju ocena 
def extract_rating(rating_str):
    try:
        if pd.isna(rating_str):
            return None
        return float(rating_str.split()[0])
    except:
        return None

df['rating'] = df['rating'].apply(extract_rating)

# 1. Razlika između najbolje i najlosije ocenjenog televizora

tvs = df[df['category'].str.contains('tv|television', case=False, na=False)]

if not tvs['rating'].dropna().empty:
    tv_rating_range = tvs['rating'].max() - tvs['rating'].min()
    print(f"Opseg ocena televizora: {tv_rating_range:.2f}")
else:
    print("Nema dostupnih ocena za televizore.")

# 2. Cenovni  opseg (IQR) za pametne telefone

smartphones = df[df['category'].str.contains('smartphone', case=False, na=False)]

if not smartphones.empty:
    q1 = smartphones['price'].quantile(0.25)
    q3 = smartphones['price'].quantile(0.75)
    iqr = q3 - q1
    print(f"Cenovni  opseg (IQR) za pametne telefone: {q1:.2f} - {q3:.2f} (IQR = {iqr:.2f})")
else:
    print("Nema podataka za pametne telefone.")

# 3. 5 brendova sa najujednacenijim ocenama 

if df['rating'].dropna().empty:
    print("Nema dostupnih ocena za izracunavanje ujednacenosti.")
else:
    brand_std = df.groupby('brand')['rating'].std().dropna()
    if brand_std.empty:
        print("Nema dovoljno podataka za izracunavanje standardne devijacije ocena po brendovima.")
    else:
        top5_brands = brand_std.sort_values().head(5)
        print("Top 5 brendova sa najujednacenijim ocenama:")
        print(top5_brands)

# 4. Da li broj dobijenih ocena zavisi od broja prodatih jedinica?

q1_num = df['num_of_ratings'].quantile(0.25)
q2_num = df['num_of_ratings'].quantile(0.50)
q3_num = df['num_of_ratings'].quantile(0.75)

def assign_quartile(num):
    if num <= q1_num:
        return '1st quartile'
    elif num <= q2_num:
        return '2nd quartile'
    elif num <= q3_num:
        return '3rd quartile'
    else:
        return '4th quartile'

df['ratings_quartile'] = df['num_of_ratings'].apply(assign_quartile)

quartile_sales = df.groupby('ratings_quartile')['quantity_sold'].sum()

print("Ukupan broj prodatih jedinica po kvartilu broja ocena:")
print(quartile_sales)
