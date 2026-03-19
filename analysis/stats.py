"""Fonctions d'analyse statistique des données d'emploi"""

import pandas as pd
import numpy as np
from collections import Counter
import logging

logger = logging.getLogger(__name__)

class JobMarketAnalyzer:
    """Analyse les données du marché de l'emploi"""
    
    def __init__(self, df):
        """
        Initialise l'analyseur avec un DataFrame.
        
        Args:
            df (pd.DataFrame): Données d'emploi
        """
        self.df = df
        self.total_jobs = len(df)
    
    def basic_stats(self):
        """Statistiques de base du dataset"""
        stats = {
            'total_offres': self.total_jobs,
            'entreprises': self.df['entreprise'].nunique(),
            'villes': self.df['ville'].nunique(),
            'regions': self.df['region'].nunique(),
        }
        
        if 'date_publication' in self.df.columns:
            stats['date_min'] = self.df['date_publication'].min()
            stats['date_max'] = self.df['date_publication'].max()
        
        return stats
    
    def top_skills(self, n=20):
        """
        Retourne les n compétences les plus demandées.
        
        Args:
            n (int): Nombre de compétences à retourner
            
        Returns:
            list: Liste de tuples (compétence, nombre)
        """
        all_skills = []
        for skills in self.df['competences_cles'].dropna():
            if isinstance(skills, str):
                all_skills.extend([s.strip() for s in skills.split('-')])
        
        return Counter(all_skills).most_common(n)
    
    def top_villes(self, n=15):
        """
        Retourne les n villes qui recrutent le plus.
        
        Args:
            n (int): Nombre de villes à retourner
            
        Returns:
            pd.Series: Series avec les villes et leurs nombres
        """
        return self.df['ville'].value_counts().head(n)
    
    def top_regions(self, n=10):
        """Top n régions"""
        return self.df['region'].value_counts().head(n)
    
    def contract_distribution(self):
        """Distribution des types de contrats"""
        return self.df['contrat'].value_counts()
    
    def experience_distribution(self):
        """Distribution des niveaux d'expérience"""
        return self.df['experience'].value_counts().head(8)
    
    def ville_categorization(self):
        """
        Catégorise les villes en groupes.
        
        Returns:
            pd.Series: Catégorie par offre
        """
        grandes_villes = ['Rabat', 'Tanger', 'Marrakech', 'Fès', 'Agadir']
        
        return self.df['ville'].apply(
            lambda x: 'Casablanca' if x == 'Casablanca' else 
                     ('Autres grandes villes' if x in grandes_villes else 'Autres villes')
        )
    
    def stats_par_ville(self):
        """
        Statistiques détaillées par ville.
        
        Returns:
            pd.DataFrame: DataFrame avec stats par ville
        """
        stats = self.df.groupby('ville').agg({
            'titre': 'count',
            'entreprise': lambda x: x.nunique(),
            'contrat': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'N/A'
        }).rename(columns={
            'titre': 'nb_offres',
            'entreprise': 'nb_entreprises_distinctes',
            'contrat': 'contrat_le_plus_courant'
        }).sort_values('nb_offres', ascending=False)
        
        return stats
    
    def heatmap_villes_contrats(self, n_villes=5, n_contrats=5):
        """
        Crée une matrice pour heatmap villes vs contrats.
        
        Args:
            n_villes (int): Nombre de top villes
            n_contrats (int): Nombre de top contrats
            
        Returns:
            pd.DataFrame: Tableau croisé pour heatmap
        """
        top_villes = self.df['ville'].value_counts().head(n_villes).index.tolist()
        top_contrats = self.df['contrat'].value_counts().head(n_contrats).index.tolist()
        
        df_filtered = self.df[
            self.df['ville'].isin(top_villes) & 
            self.df['contrat'].isin(top_contrats)
        ]
        
        return pd.crosstab(df_filtered['ville'], df_filtered['contrat'])

    def export_stats(self, filename):
        """
        Exporte les statistiques dans un fichier texte.
        
        Args:
            filename (str): Chemin du fichier de sortie
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("RAPPORT D'ANALYSE DU MARCHÉ DE L'EMPLOI\n")
            f.write("="*60 + "\n\n")
            
            # Statistiques générales
            f.write("📊 STATISTIQUES GÉNÉRALES\n")
            f.write("-"*40 + "\n")
            stats = self.basic_stats()
            for key, value in stats.items():
                f.write(f"{key:15}: {value}\n")
            f.write("\n")
            
            # Top compétences
            f.write("🏆 TOP 15 COMPÉTENCES\n")
            f.write("-"*40 + "\n")
            skills = self.top_skills(15)
            for skill, count in skills:
                f.write(f"{skill:30} {count}\n")
            f.write("\n")
            
            # Top régions
            f.write("📍 TOP 10 RÉGIONS\n")
            f.write("-"*40 + "\n")
            regions = self.top_regions(10)
            for region, count in regions.items():
                if pd.notna(region):
                    f.write(f"{region:35} {count}\n")
            f.write("\n")
            
            # Types de contrats
            f.write("📋 TYPES DE CONTRATS\n")
            f.write("-"*40 + "\n")
            contracts = self.contract_distribution()
            for contract, count in contracts.items():
                if pd.notna(contract):
                    f.write(f"{contract:15} {count}\n")
        
        print(f"✅ Rapport sauvegardé: {filename}")