import logging
import time
import json
import psutil
import platform
from datetime import datetime
from pathlib import Path

class PipelineMonitor:
    """Monitor les performances du pipeline"""
    
    def __init__(self, log_dir='logs'):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / 'pipeline.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def log_system_info(self):
        """Log les informations système"""
        info = {
            'timestamp': datetime.now().isoformat(),
            'system': platform.system(),
            'release': platform.release(),
            'processor': platform.processor(),
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total / (1024**3),
            'memory_available': psutil.virtual_memory().available / (1024**3)
        }
        self.logger.info(f"System info: {json.dumps(info)}")
        return info
    
    def log_pipeline_execution(self, func):
        """Décorateur pour monitorer l'exécution"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024**2
            
            self.logger.info(f"Début de {func.__name__}")
            
            try:
                result = func(*args, **kwargs)
                
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss / 1024**2
                
                metrics = {
                    'function': func.__name__,
                    'duration': round(end_time - start_time, 2),
                    'memory_start_mb': round(start_memory, 2),
                    'memory_end_mb': round(end_memory, 2),
                    'memory_delta_mb': round(end_memory - start_memory, 2),
                    'timestamp': datetime.now().isoformat()
                }
                
                self.logger.info(f"Métriques: {json.dumps(metrics)}")
                self._save_metrics(metrics)
                
                return result
                
            except Exception as e:
                self.logger.error(f"Erreur dans {func.__name__}: {str(e)}")
                raise
                
        return wrapper
    
    def _save_metrics(self, metrics):
        """Sauvegarde les métriques"""
        metrics_file = self.log_dir / 'metrics.jsonl'
        with open(metrics_file, 'a') as f:
            f.write(json.dumps(metrics) + '\n')
    
    def generate_report(self):
        """Génère un rapport"""
        metrics_file = self.log_dir / 'metrics.jsonl'
        if not metrics_file.exists():
            return "Aucune métrique disponible"
        
        with open(metrics_file, 'r') as f:
            lines = f.readlines()
        
        total_time = 0
        executions = len(lines)
        
        for line in lines:
            data = json.loads(line)
            total_time += data.get('duration', 0)
        
        report = f"""
        📊 RAPPORT DE PERFORMANCE
        ========================
        Exécutions: {executions}
        Temps total: {total_time:.2f}s
        Temps moyen: {total_time/executions:.2f}s
        """
        
        self.logger.info(report)
        return report