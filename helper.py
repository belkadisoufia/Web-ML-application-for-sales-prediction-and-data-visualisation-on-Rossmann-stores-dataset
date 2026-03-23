import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import pickle
import math

# Charger le store déjà nettoyé dans le Notebook
def store_data():
    return pd.read_csv('./data/store_cleaned.csv')

def easter_data():
    return pd.read_csv('./data/Easter_dates_data.csv')

def isStateHoliday(sales_date, easter_df):
    year = sales_date.year
    e_row = easter_df[easter_df['Year'] == year]
    if e_row.empty: return 0
    
    easter_date = datetime(year, int(e_row['Month'].values[0]), int(e_row['Day'].values[0]))
    
    # Jours fériés fixes
    if (sales_date.month == 1 and sales_date.day in [1, 6] or
        sales_date.month == 5 and sales_date.day == 1 or
        sales_date.month == 12 and sales_date.day in [25, 26]):
        return 1
    # Jours fériés mobiles
    if (sales_date == easter_date - timedelta(days=3) or sales_date == easter_date + timedelta(days=1) or
        sales_date == easter_date + timedelta(days=38) or sales_date == easter_date + timedelta(days=49) or
        sales_date == easter_date + timedelta(days=59)):
        return 1
    return 0

def get_total_sales(store_id, from_date, to_date, store_df, easter_df, ml_model, encoder):
    # 1. Création de la plage de dates
    dates = pd.date_range(from_date, to_date)
    
    # 2. Récupération des infos du magasin
    store_info = store_df[store_df['Store'] == store_id].iloc[0]
    
    # 3. Construction du tableau de prédiction
    df = pd.DataFrame({'Date': dates})
    df['DayOfWeek'] = df['Date'].dt.weekday + 1
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['WeekOfYear'] = df['Date'].dt.isocalendar().week.astype(int)
    
    # Injecter les données du store
    for col in store_df.columns:
        if col != 'Store': 
            df[col] = store_info[col]

    # Caractéristiques temporelles
    df['StateHoliday'] = df['Date'].apply(lambda x: isStateHoliday(x, easter_df))
    df['SchoolHoliday'] = 0
    df['Open'] = df['DayOfWeek'].apply(lambda x: 1 if x < 7 else 0)

    # Nouvelles variables
    df['CompetitionOpenNumMonths'] = (df['Year'] - df['CompetitionOpenSinceYear']) * 12 + (df['Month'] - df['CompetitionOpenSinceMonth'])
    df['CompetitionOpenNumMonths'] = df['CompetitionOpenNumMonths'].clip(lower=0)
    df['Promo2NumWeeks'] = (df['Year'] - df['Promo2SinceYear']) * 52 + (df['WeekOfYear'] - df['Promo2SinceWeek'])
    df.loc[df['Promo2'] == 0, 'Promo2NumWeeks'] = 0
    df['Promo2NumWeeks'] = df['Promo2NumWeeks'].clip(lower=0)

    # Transformations
    df['CompetitionOpenNumMonths'] = np.sqrt(df['CompetitionOpenNumMonths'])
    df['Promo2NumWeeks'] = np.sqrt(df['Promo2NumWeeks'])
    df['CompetitionDistance'] = np.log(df['CompetitionDistance'])

    # Encodage binaire
    df['DayOfWeek_0'] = df['DayOfWeek'].apply(lambda x: 1 if x in [1, 2, 6, 7] else 0)
    df['DayOfWeek_1'] = df['DayOfWeek'].apply(lambda x: 1 if x in [3, 4, 6, 7] else 0)
    df['DayOfWeek_2'] = df['DayOfWeek'].apply(lambda x: 1 if x in [1, 3, 5, 6] else 0)
    
    df['WeekOfYear_0'] = df['WeekOfYear'].apply(lambda x: 1 if x >= 32 else 0)
    df['WeekOfYear_1'] = df['WeekOfYear'].apply(lambda x: 1 if x <= 16 or (32 <= x <= 36) else 0)
    df['WeekOfYear_2'] = df['WeekOfYear'].apply(lambda x: 1 if x <= 8 or (17 <= x <= 24) or (37 <= x <= 44) else 0)
    df['WeekOfYear_3'] = df['WeekOfYear'].apply(lambda x: 1 if math.ceil(x / 4) % 2 != 0 else 0)
    df['WeekOfYear_4'] = df['WeekOfYear'].apply(lambda x: 1 if math.ceil(x / 2) % 2 != 0 else 0)
    df['WeekOfYear_5'] = df['WeekOfYear'].apply(lambda x: 1 if x % 2 != 0 else 0)

    # One Hot Encoding
    encoded_cols = encoder.transform(df[['StoreType', 'Assortment']])
    feature_names = encoder.get_feature_names_out(['StoreType', 'Assortment'])
    for i, col_name in enumerate(feature_names):
        df[col_name] = encoded_cols[:, i]

    # Promo Interval
    if 'PromoInterval' in df.columns:
        promo_dummies = pd.get_dummies(df['PromoInterval'], prefix='PromoInterval')
        df = pd.concat([df, promo_dummies], axis=1)
        df.drop(columns=['PromoInterval'], inplace=True)

    # IMPORTANT: Garder une trace des colonnes avant suppression
    print(f" Colonnes avant suppression: {list(df.columns)}")
    
    # Colonnes à supprimer
    cols_to_drop = ['Date', 'DayOfWeek', 'WeekOfYear', 'Month', 'Year', 
                    'StoreType', 'Assortment', 'CompetitionOpenSinceMonth', 
                    'CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek', 
                    'Promo2SinceYear']
    
    # Ne supprimer que les colonnes qui existent
    cols_to_drop = [c for c in cols_to_drop if c in df.columns]
    if cols_to_drop:
        df.drop(columns=cols_to_drop, inplace=True)
    
    # S'assurer que toutes les colonnes sont numériques
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Vérifier les colonnes finales
    print(f"Colonnes finales ({len(df.columns)}): {list(df.columns)}")
    
    # Prédiction
    try:
        # Essayer avec les noms de colonnes
        preds = np.square(ml_model.predict(df))
    except Exception as e:
        print(f"Erreur avec noms de colonnes: {e}")
        print("Tentative avec les valeurs numpy uniquement...")
        # Essayer sans les noms de colonnes
        preds = np.square(ml_model.predict(df.values))
    
    return dict(zip(dates, preds))