"""Génération de rapports d'analyse"""

import pandas as pd
from datetime import datetime
import os
from .stats import JobMarketAnalyzer

def generate_ville_report(analyzer, output_dir='analysis/reports'):
    """
    Génère un rapport détaillé sur l'analyse des villes.
    
    Args:
        analyzer (JobMarketAnalyzer): Instance de l'analyseur
        output_dir (str): Dossier de sortie
    """
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{output_dir}/rapport_villes_{timestamp}.txt'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("RAPPORT D'ANALYSE DES VILLES\n")
        f.write(f"Généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("="*60 + "\n\n")
        
        # Statistiques générales
        f.write("📊 STATISTIQUES GÉNÉRALES\n")
        f.write("-"*40 + "\n")
        stats = analyzer.basic_stats()
        for key, value in stats.items():
            f.write(f"{key:15}: {value}\n")
        f.write("\n")
        
        # Top 15 villes
        f.write("🏙️ TOP 15 VILLES\n")
        f.write("-"*40 + "\n")
        top_villes = analyzer.top_villes(15)
        for i, (ville, count) in enumerate(top_villes.items(), 1):
            pourcentage = (count / analyzer.total_jobs) * 100
            f.write(f"{i:2}. {ville:25} {count:3} ({pourcentage:.1f}%)\n")
        f.write("\n")
        
        # Catégorisation
        f.write("📊 CATÉGORISATION DES VILLES\n")
        f.write("-"*40 + "\n")
        categories = analyzer.ville_categorization().value_counts()
        for cat, count in categories.items():
            pourcentage = (count / analyzer.total_jobs) * 100
            f.write(f"{cat:20}: {count} ({pourcentage:.1f}%)\n")
        f.write("\n")
        
        # Statistiques détaillées
        f.write("📈 STATISTIQUES DÉTAILLÉES PAR VILLE\n")
        f.write("-"*40 + "\n")
        stats_ville = analyzer.stats_par_ville().head(10)
        f.write(stats_ville.to_string())
    
    print(f"✅ Rapport sauvegardé: {filename}")
    return filename

def generate_comparison_chart_data(analyzer):
    """
    Génère les données pour le graphique de comparaison.
    
    Returns:
        dict: Données pour le graphique
    """
    categories = analyzer.ville_categorization().value_counts()
    
    return {
        'labels': categories.index.tolist(),
        'values': categories.values.tolist(),
        'total': analyzer.total_jobs
    }

def generate_report(df, output_file=None):
    """
    Génère un rapport complet au format markdown (pour compatibilité).
    
    Args:
        df (pd.DataFrame): Données analysées
        output_file (str): Fichier de sortie
    """
    if output_file is None:
        output_file = f"report_{datetime.now().strftime('%Y%m%d')}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# 📊 Rapport d'Analyse du Marché de l'Emploi\n")
        f.write(f"*Généré le {datetime.now().strftime('%d/%m/%Y')}*\n\n")
        
        # Stats générales
        f.write("## 📈 Vue d'ensemble\n\n")
        f.write(f"- **Total offres** : {len(df)}\n")
        f.write(f"- **Entreprises** : {df['entreprise'].nunique()}\n")
        f.write(f"- **Villes** : {df['ville'].nunique()}\n")
        f.write(f"- **Régions** : {df['region'].nunique()}\n\n")
        
        # Top villes
        f.write("## 🏙️ Top 10 Villes\n\n")
        f.write("| Ville | Offres | % |\n")
        f.write("|-------|--------|---|\n")
        for ville, count in df['ville'].value_counts().head(10).items():
            pct = (count/len(df))*100
            f.write(f"| {ville} | {count} | {pct:.1f}% |\n")
    
    print(f"✅ Rapport généré: {output_file}")
    return output_file