#!/usr/bin/env python
"""Script pour tester les métriques"""

from prometheus_client import start_http_server, Counter
import time
import random

# Créer une métrique simple
jobs = Counter('jobs_collected_total', 'Total jobs collected')

def main():
    # Démarrer le serveur sur le port 8001 pour ne pas interférer
    start_http_server(8001)
    print("✅ Serveur de métriques sur http://localhost:8001/metrics")
    
    # Simuler des collectes
    while True:
        jobs.inc(random.randint(1, 10))
        print(f"➕ {jobs._value.get()} jobs collectés")
        time.sleep(5)

if __name__ == "__main__":
    main()