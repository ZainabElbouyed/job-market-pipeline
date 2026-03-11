"""Module de transformation des données"""

import pandas as pd
import logging
from collections import Counter

logger = logging.getLogger(__name__)

class DataTransformer:
    """Transforme les données pour l'analyse"""
    
    def transform(self, df):
        """
        Applique les transformations.
        
        Args:
            df (pd.DataFrame): Données nettoyées
            
        Returns:
            pd.DataFrame: Données transformées
        """
        logger.info("Début des transformations...")
        df_trans = df.copy()
        
        # Créer une colonne avec la liste des compétences
        if 'competences_cles' in df_trans.columns:
            df_trans['skills_list'] = df_trans['competences_cles'].apply(
                lambda x: [s.strip() for s in x.split('-')] if isinstance(x, str) else []
            )
        
        # Catégoriser l'expérience
        if 'experience' in df_trans.columns:
            df_trans['experience_cat'] = df_trans['experience'].apply(
                self._categorize_experience
            )
        
        # Ajouter des métadonnées
        df_trans['annee'] = pd.DatetimeIndex(df_trans['date_publication']).year
        df_trans['mois'] = pd.DatetimeIndex(df_trans['date_publication']).month
        
        logger.info("Transformations terminées")
        return df_trans
    
    def _categorize_experience(self, exp):
        """Catégorise le niveau d'expérience"""
        if not isinstance(exp, str):
            return 'Non spécifié'
        
        if 'Débutant' in exp or '< 2' in exp:
            return 'Débutant'
        elif '2 ans' in exp and '5 ans' in exp:
            return 'Junior (2-5 ans)'
        elif '5 ans' in exp and '10 ans' in exp:
            return 'Confirmé (5-10 ans)'
        elif '10' in exp:
            return 'Senior (>10 ans)'
        else:
            return 'Non spécifié'
    
    def extract_top_skills(self, df, n=20):
        """Extrait les n compétences les plus fréquentes"""
        all_skills = []
        for skills in df['skills_list']:
            all_skills.extend(skills)
        
        return Counter(all_skills).most_common(n)