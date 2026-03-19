#!/usr/bin/env python
"""Planificateur pour exécutions automatiques"""

import schedule
import time
import argparse
import subprocess
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    """Exécute le pipeline complet"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"🚀 Exécution programmée: {timestamp}")
    
    try:
        subprocess.run(['python', 'scripts/run_pipeline.py', '--pages', '30', '--visuals'], 
                      check=True)
        logging.info("✅ Exécution réussie")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Erreur: {e}")

def main():
    parser = argparse.ArgumentParser(description='Planificateur de scraping')
    parser.add_argument('--once', action='store_true', help='Exécuter une fois après délai')
    parser.add_argument('--delay', type=int, default=3600, help='Délai en secondes')
    parser.add_argument('--daily', action='store_true', help='Exécution quotidienne')
    parser.add_argument('--time', type=str, default='09:00', help='Heure pour quotidien')
    parser.add_argument('--interval', type=int, help='Intervalle en secondes')
    
    args = parser.parse_args()
    
    if args.once:
        logging.info(f"⏰ Exécution unique dans {args.delay} secondes")
        time.sleep(args.delay)
        run_pipeline()
    
    elif args.daily:
        schedule.every().day.at(args.time).do(run_pipeline)
        logging.info(f"📅 Planifié quotidiennement à {args.time}")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    elif args.interval:
        schedule.every(args.interval).seconds.do(run_pipeline)
        logging.info(f"🔄 Planifié toutes les {args.interval} secondes")
        
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()