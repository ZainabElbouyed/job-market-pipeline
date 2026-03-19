from prometheus_client import start_http_server, Counter, Gauge, Histogram
import time
import random
import psutil

# Métriques
scraping_duration = Histogram('scraping_duration_seconds', 'Temps de scraping')
jobs_collected = Counter('jobs_collected_total', 'Nombre total d\'offres collectées')
errors_total = Counter('errors_total', 'Nombre total d\'erreurs')
memory_usage = Gauge('memory_usage_bytes', 'Utilisation mémoire')
disk_usage = Gauge('disk_usage_bytes', 'Utilisation disque')

def collect_system_metrics():
    """Collecte les métriques système"""
    memory_usage.set(psutil.virtual_memory().used)
    disk_usage.set(psutil.disk_usage('/').used)

def start_metrics_server(port=8000):
    """Démarre le serveur de métriques"""
    start_http_server(port)
    print(f"✅ Serveur de métriques démarré sur le port {port}")
    
    while True:
        collect_system_metrics()
        time.sleep(15)

if __name__ == "__main__":
    start_metrics_server()