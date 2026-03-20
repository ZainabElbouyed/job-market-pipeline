# scripts/metrics.py
from prometheus_client import Counter, Histogram, Gauge, push_to_gateway
import psutil
import os
from datetime import datetime

# Configuration
PUSHGATEWAY_URL = 'http://localhost:9091'  # Par défaut, Pushgateway tourne sur ce port

# Définition des métriques
scraping_duration = Histogram('scraping_duration_seconds', 'Temps de scraping')
jobs_collected = Counter('jobs_collected_total', 'Nombre total d\'offres collectées')
errors_total = Counter('errors_total', 'Nombre total d\'erreurs')
memory_usage = Gauge('memory_usage_bytes', 'Utilisation mémoire')
disk_usage = Gauge('disk_usage_bytes', 'Utilisation disque')

def update_system_metrics():
    """Met à jour les métriques système"""
    memory_usage.set(psutil.virtual_memory().used)
    disk_usage.set(psutil.disk_usage('/').used)

def record_scraping_result(jobs_count, duration, error_count=0):
    """Enregistre les résultats d'un scraping"""
    jobs_collected.inc(jobs_count)
    scraping_duration.observe(duration)
    if error_count > 0:
        errors_total.inc(error_count)
    
    os.makedirs('logs', exist_ok=True)
    with open('logs/metrics.log', 'a') as f:
        f.write(f"{datetime.now().isoformat()},{jobs_count},{duration},{error_count}\n")

    # Envoyer les métriques à Prometheus via Pushgateway
    try:
        push_to_gateway(
            PUSHGATEWAY_URL,
            job='job-market-pipeline',
            registry=None  # Utilise le registre par défaut
        )
        print(f"📊 Métriques envoyées: {jobs_count} offres, {duration:.2f}s")
    except Exception as e:
        print(f"⚠️ Pushgateway non disponible: {e} (métriques seulement en local)")