import sys
import os
import argparse
import shutil
from pathlib import Path
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.monitoring import PipelineMonitor
from scripts.run_pipeline import main as run_pipeline

def setup_production_environment():
    """Configure l'environnement de production"""
    
    dirs = [
        'data/raw',
        'data/processed',
        'logs',
        'backups'
    ]
    
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"✅ Dossier créé: {d}")
    
    print("✅ Environnement de production configuré")

def backup_data():
    """Sauvegarde les données"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = f'backups/backup_{timestamp}'
    
    if Path('data').exists():
        shutil.copytree('data', backup_dir)
        print(f"✅ Données sauvegardées dans {backup_dir}")
    
    # Nettoyer les vieux backups (> 7 jours)
    import time
    now = time.time()
    for backup in Path('backups').glob('backup_*'):
        if backup.is_dir() and now - backup.stat().st_mtime > 7 * 86400:
            shutil.rmtree(backup)
            print(f"🧹 Ancien backup supprimé: {backup}")

def main():
    parser = argparse.ArgumentParser(description='Pipeline de production')
    parser.add_argument('--pages', type=int, default=30, help='Nombre de pages')
    parser.add_argument('--setup', action='store_true', help='Configurer environnement')
    parser.add_argument('--backup', action='store_true', help='Sauvegarder les données')
    
    args = parser.parse_args()
    
    monitor = PipelineMonitor()
    
    if args.setup:
        setup_production_environment()
        return
    
    if args.backup:
        backup_data()
        return
    
    @monitor.log_pipeline_execution
    def run_with_monitoring():
        # Exécuter le pipeline
        sys.argv = ['run_pipeline.py', '--pages', str(args.pages), '--visuals']
        run_pipeline()
    
    run_with_monitoring()
    backup_data()
    monitor.generate_report()

if __name__ == "__main__":
    main()