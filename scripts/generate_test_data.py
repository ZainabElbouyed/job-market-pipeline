#!/usr/bin/env python
"""Génère des données de test pour GitHub Pages"""

import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from visualization.plots import JobMarketVisualizer

def main():
    print("🔧 Génération des données de test...")
    
    # Créer les dossiers
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('visualization/outputs', exist_ok=True)
    
    # Données synthétiques
    np.random.seed(42)
    n_jobs = 200
    
    # Villes
    villes = ['Casablanca', 'Rabat', 'Tanger', 'Marrakech', 'Agadir', 'Fès']
    probs = [0.4, 0.2, 0.15, 0.1, 0.08, 0.07]
    
    # Compétences
    competences = [
        'Python - SQL - Pandas',
        'JavaScript - React - Node.js',
        'Docker - Kubernetes - AWS',
        'Java - Spring - Hibernate',
        'Data Science - Machine Learning'
    ]
    
    # Création du DataFrame
    df = pd.DataFrame({
        'titre': np.random.choice(
            ['Data Scientist', 'Data Engineer', 'DevOps', 'Développeur Full Stack', 
             'Data Analyst', 'Cloud Architect'], n_jobs),
        'entreprise': np.random.choice(
            ['Tech Corp', 'Data Solutions', 'AI Labs', 'Startup XYZ', 'Digital Factory'], n_jobs),
        'ville': np.random.choice(villes, n_jobs, p=probs),
        'contrat': np.random.choice(['CDI', 'CDD', 'Freelance', 'Stage'], n_jobs, p=[0.6, 0.2, 0.15, 0.05]),
        'competences_cles': np.random.choice(competences, n_jobs),
    })
    
    # Ajouter région
    region_map = {
        'Casablanca': 'Casablanca-Mohammedia',
        'Rabat': 'Rabat-Salé-Kénitra',
        'Tanger': 'Tanger-Tétouan',
        'Marrakech': 'Marrakech-Safi',
        'Agadir': 'Souss-Massa',
        'Fès': 'Fès-Meknès'
    }
    df['region'] = df['ville'].map(region_map)
    
    # Ajouter expérience
    df['experience'] = np.random.choice(
        ['Débutant', 'Junior (2-5 ans)', 'Confirmé (5-10 ans)', 'Senior (>10 ans)'], n_jobs
    )
    
    # Sauvegarder
    df.to_csv('data/processed/jobs_clean.csv', index=False)
    print(f"✅ {n_jobs} offres de test générées")
    
    # Générer les graphiques
    viz = JobMarketVisualizer(df)
    viz.output_dir = 'visualization/outputs'
    viz.create_all_ville_plots()
    print(f"✅ Graphiques générés dans visualization/outputs/")

if __name__ == "__main__":
    main()