#!/usr/bin/env python
"""Script pour exécuter le scraping seul"""

import argparse
import sys
import os

# Ajouter le chemin absolu du projet
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)  # Ajoute au début du path

print(f"📁 Répertoire du projet: {PROJECT_ROOT}")

# Maintenant on peut importer
from scraper.scraper import EmploiMaScraper

def main():
    parser = argparse.ArgumentParser(description='Scraper Emploi.ma')
    parser.add_argument('--pages', type=int, default=30, help='Nombre de pages à scraper')
    parser.add_argument('--sample', type=int, help='Taille de l\'échantillon')
    
    args = parser.parse_args()
    
    print("="*60)
    print("🚀 SCRAPER EMPLOI.MA")
    print("="*60)
    print(f"📄 Pages: {args.pages}")
    
    # Changer vers le répertoire du projet
    os.chdir(PROJECT_ROOT)
    print(f"📂 Répertoire de travail: {os.getcwd()}")
    
    scraper = EmploiMaScraper()
    df = scraper.run(max_pages=args.pages, sample=args.sample)
    
    print(f"\n✅ Scraping terminé: {len(df)} offres")

if __name__ == "__main__":
    main()