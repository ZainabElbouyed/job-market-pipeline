"""Module de nettoyage des données"""

import pandas as pd
import re
import logging

logger = logging.getLogger(__name__)

class DataCleaner:
    """Nettoie les données brutes du scraping"""
    
    def __init__(self):
        self.required_columns = [
            'titre', 'entreprise', 'date_publication', 'region',
            'ville', 'contrat', 'experience', 'niveau_etude',
            'competences_cles', 'url'
        ]
    
    def clean(self, df):
        """
        Nettoie le DataFrame.
        
        Args:
            df (pd.DataFrame): Données brutes
            
        Returns:
            pd.DataFrame: Données nettoyées
        """
        logger.info("Début du nettoyage...")
        df_clean = df.copy()
        
        # Suppression des doublons
        initial_len = len(df_clean)
        df_clean.drop_duplicates(subset=['url'], inplace=True)
        logger.info(f"Doublons supprimés: {initial_len - len(df_clean)}")
        
        # Remplacer les valeurs nulles
        for col in self.required_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].fillna('Non spécifié')
        
        # Nettoyer les villes
        if 'ville' in df_clean.columns:
            df_clean['ville'] = df_clean['ville'].str.strip()
            df_clean['ville'] = df_clean['ville'].replace('', 'Non spécifiée')
        
        # Standardiser les dates
        if 'date_publication' in df_clean.columns:
            df_clean['date_publication'] = pd.to_datetime(
                df_clean['date_publication'], 
                errors='coerce',
                format='%d.%m.%Y'
            )
        
        logger.info(f"Nettoyage terminé: {len(df_clean)} lignes")
        return df_clean
    
    def remove_outliers(self, df, column, threshold=100):
        """Supprime les outliers basés sur un seuil"""
        if column in df.columns:
            value_counts = df[column].value_counts()
            rare_values = value_counts[value_counts < threshold].index
            df.loc[df[column].isin(rare_values), column] = 'Autre'
        return df