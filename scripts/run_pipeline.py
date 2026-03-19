#!/usr/bin/env python
"""Pipeline complet d'analyse"""

import argparse
import sys
import os
import pandas as pd
from datetime import datetime
import logging
from metrics import record_scraping_result, update_system_metrics
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.scraper import EmploiMaScraper
from pipeline.cleaner import DataCleaner
from pipeline.transformer import DataTransformer
from analysis.stats import JobMarketAnalyzer
from analysis.reports import generate_report
from visualization.plots import JobMarketVisualizer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Pipeline complet d\'analyse')
    parser.add_argument('--pages', type=int, default=30, help='Nombre de pages')
    parser.add_argument('--sample', type=int, help='Taille échantillon')
    parser.add_argument('--no-scrape', action='store_true', help='Utiliser données existantes')
    parser.add_argument('--visuals', action='store_true', help='Générer visuels')
    
    args = parser.parse_args()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 1. SCRAPING
    if not args.no_scrape:
        logger.info("🚀 Phase 1: Scraping")

        start_time = time.time() 

        scraper = EmploiMaScraper()
        df = scraper.run(max_pages=args.pages, sample=args.sample)
        
        duration = time.time() - start_time
        
        if len(df) == 0:
            logger.error("❌ Aucune donnée collectée - Arrêt du pipeline")
            record_scraping_result(0, duration, error_count=1)
            return
        
        # Enregistrer les métriques
        record_scraping_result(len(df), duration)
        update_system_metrics()

        # Sauvegarde (maintenant que df n'est pas vide)
        raw_file = f'data/raw/jobs_{timestamp}.csv'
        os.makedirs('data/raw', exist_ok=True)
        df.to_csv(raw_file, index=False)
        logger.info(f"✅ Données brutes: {raw_file} ({len(df)} offres)")
    else:
        # Charger dernier fichier
        import glob
        files = glob.glob('data/raw/jobs_*.csv')
        if not files:
            logger.error("❌ Aucun fichier trouvé")
            return
        latest = max(files, key=os.path.getctime)
        df = pd.read_csv(latest)
        logger.info(f"📂 Données chargées: {latest}")
    
    # 2. PIPELINE
    logger.info("🔧 Phase 2: Nettoyage et transformation")
    cleaner = DataCleaner()
    df_clean = cleaner.clean(df)
    
    transformer = DataTransformer()
    df_final = transformer.transform(df_clean)
    
    clean_file = f'data/processed/jobs_clean_{timestamp}.csv'
    df_final.to_csv(clean_file, index=False)
    logger.info(f"✅ Données nettoyées: {clean_file}")
    
    # 3. ANALYSE
    logger.info("📊 Phase 3: Analyse statistique")
    analyzer = JobMarketAnalyzer(df_final)
    analyzer.basic_stats()
    analyzer.top_skills(15)
    analyzer.top_regions()
    
    report_file = f'analysis/reports/report_{timestamp}.txt'
    analyzer.export_stats(report_file)
    
    # 4. VISUALISATION
    if args.visuals:
        logger.info("🎨 Phase 4: Création des visualisations")
        viz = JobMarketVisualizer(df_final)
        viz.output_dir = f'visualization/outputs/{timestamp}'
        os.makedirs(viz.output_dir, exist_ok=True)
        viz.create_all_ville_plots()
    
    logger.info("✅ Pipeline terminé avec succès!")

if __name__ == "__main__":
    main()