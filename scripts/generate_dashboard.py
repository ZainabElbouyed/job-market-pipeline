#!/usr/bin/env python
"""Génère le dashboard avec les vraies données"""

import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from visualization.plots import JobMarketVisualizer

def main():
    print("📊 Génération du dashboard avec les vraies données...")
    
    # Créer les dossiers
    os.makedirs('visualization/outputs', exist_ok=True)
    
    # Charger LES VRAIES DONNÉES
    real_file = 'data/processed/jobs_real.csv'
    
    if os.path.exists(real_file):
        df = pd.read_csv(real_file)
        print(f"✅ Fichier réel chargé: {len(df)} offres")
    else:
        # Fallback sur les données de test si le fichier n'existe pas
        print("⚠️ Fichier réel non trouvé, utilisation des données de test")
        from scripts.generate_test_data import generate_test_data
        df = generate_test_data()
    
    # Générer les visualisations
    viz = JobMarketVisualizer(df)
    viz.output_dir = 'visualization/outputs'
    viz.create_all_ville_plots()
    print(f"✅ Graphiques générés dans visualization/outputs/")

if __name__ == "__main__":
    main()