#!/usr/bin/env python
"""Génère le dashboard avec les vraies données (dernier fichier)"""

import pandas as pd
import os
import sys
import glob
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from visualization.plots import JobMarketVisualizer

def get_latest_file(directory, pattern):
    """Retourne le fichier le plus récent correspondant au pattern"""
    files = glob.glob(os.path.join(directory, pattern))
    if not files:
        return None
    return max(files, key=os.path.getctime)

def main():
    print("📊 Génération du dashboard avec les dernières données...")
    
    # Créer les dossiers
    os.makedirs('visualization/outputs', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    # MÉTHODE 1: Chercher le dernier fichier nettoyé dans data/processed/
    latest_clean = get_latest_file('data/processed', 'jobs_clean_*.csv')
    
    # MÉTHODE 2: Chercher le dernier fichier brut dans data/raw/
    latest_raw = get_latest_file('data/raw', 'jobs_*.csv')
    
    # MÉTHODE 3: Chercher le fichier jobs_real.csv
    real_file = 'data/processed/jobs_real.csv'
    
    df = None
    source = None
    
    # Priorité 1: Dernier fichier nettoyé
    if latest_clean:
        df = pd.read_csv(latest_clean)
        source = latest_clean
        print(f"✅ Données chargées: {source}")
        print(f"   📊 {len(df)} offres")
    
    # Priorité 2: Dernier fichier brut
    elif latest_raw:
        df = pd.read_csv(latest_raw)
        source = latest_raw
        print(f"✅ Données brutes chargées: {source}")
        print(f"   📊 {len(df)} offres")
    
    # Priorité 3: Fichier jobs_real.csv
    elif os.path.exists(real_file):
        df = pd.read_csv(real_file)
        source = real_file
        print(f"✅ Données chargées: {source}")
        print(f"   📊 {len(df)} offres")
    
    # Fallback: générer des données de test
    else:
        print("⚠️ Aucune donnée trouvée - génération de données de test")
        print("   Recherche effectuée dans:")
        print("   • data/processed/jobs_clean_*.csv")
        print("   • data/raw/jobs_*.csv")
        print("   • data/processed/jobs_real.csv")
        
        from scripts.generate_test_data import generate_test_data
        df = generate_test_data()
        source = "test_data"
        print(f"✅ Données de test générées: {len(df)} offres")
    
    # Afficher un aperçu des données
    if df is not None:
        print(f"\n📋 Aperçu des données:")
        print(f"   • Villes: {df['ville'].nunique()}")
        print(f"   • Entreprises: {df['entreprise'].nunique()}")
        print(f"   • Contrats: {df['contrat'].value_counts().to_dict()}")
    
    # Générer les visualisations
    print("\n🎨 Génération des visualisations...")
    viz = JobMarketVisualizer(df)
    viz.output_dir = 'visualization/outputs'
    viz.create_all_ville_plots()
    
    print(f"\n✅ Graphiques générés dans visualization/outputs/")
    print(f"   Source: {source}")

if __name__ == "__main__":
    main()