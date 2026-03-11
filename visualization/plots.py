"""Fonctions de visualisation des données"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
from .styles import configure_styles

# Configuration des styles
configure_styles()

class JobMarketVisualizer:
    """Classe pour créer toutes les visualisations"""
    
    def __init__(self, df, output_dir='visualization/outputs'):
        """
        Initialise le visualiseur.
        
        Args:
            df (pd.DataFrame): Données à visualiser
            output_dir (str): Dossier de sortie pour les images
        """
        self.df = df
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_top_villes(self, n=15, save=True):
        """
        Crée un graphique des top villes.
        
        Args:
            n (int): Nombre de villes à afficher
            save (bool): Sauvegarder l'image
        """
        # Nettoyer les données
        self.df['ville'] = self.df['ville'].fillna('Non spécifiée').str.strip()
        ville_counts = self.df['ville'].value_counts().head(n)
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(14, 8))
        colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(ville_counts)))
        
        bars = ax.barh(range(len(ville_counts)), ville_counts.values, 
                      color=colors, edgecolor='navy', linewidth=0.5)
        
        ax.set_yticks(range(len(ville_counts)))
        ax.set_yticklabels(ville_counts.index, fontsize=11)
        ax.set_xlabel('Nombre d\'offres', fontsize=13, fontweight='bold')
        ax.set_title(f'Top {n} des Villes qui Recrutent au Maroc', 
                    fontsize=18, fontweight='bold', pad=20)
        ax.invert_yaxis()
        
        # Ajouter les valeurs
        total = len(self.df)
        for bar, count in zip(bars, ville_counts.values):
            pourcentage = (count / total) * 100
            ax.text(count + 0.5, bar.get_y() + bar.get_height()/2, 
                   f'{count} ({pourcentage:.1f}%)', 
                   va='center', fontweight='bold', fontsize=10)
        
        ax.grid(True, axis='x', alpha=0.3)
        plt.tight_layout()
        
        if save:
            filename = f'{self.output_dir}/top_{n}_villes.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ Graphique sauvegardé: {filename}")
        
        plt.show()
    
    def plot_ville_comparison(self, save=True):
        """
        Crée un graphique comparant Casablanca aux autres villes.
        
        Args:
            save (bool): Sauvegarder l'image
        """
        # Catégoriser les villes
        grandes_villes = ['Rabat', 'Tanger', 'Marrakech', 'Fès', 'Agadir']
        
        self.df['ville_categorie'] = self.df['ville'].apply(
            lambda x: 'Casablanca' if x == 'Casablanca' else 
                     ('Autres grandes villes' if x in grandes_villes else 'Autres villes')
        )
        
        categorie_counts = self.df['ville_categorie'].value_counts()
        
        # Créer la figure avec deux sous-graphiques
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # Camembert
        colors_pie = plt.cm.Set3(np.linspace(0, 1, len(categorie_counts)))
        wedges, texts, autotexts = ax1.pie(
            categorie_counts.values, 
            labels=categorie_counts.index,
            autopct='%1.1f%%',
            colors=colors_pie,
            textprops={'fontsize': 12, 'fontweight': 'bold'},
            wedgeprops={'edgecolor': 'white', 'linewidth': 1}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
        
        ax1.set_title('Répartition: Casablanca vs Autres Villes', 
                     fontsize=16, fontweight='bold')
        
        # Diagramme en barres
        colors_bar = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        bars = ax2.bar(categorie_counts.index, categorie_counts.values, 
                       color=colors_bar, edgecolor='navy', linewidth=0.5)
        
        ax2.set_ylabel('Nombre d\'offres', fontsize=12, fontweight='bold')
        ax2.set_title('Comparaison du Nombre d\'Offres', 
                     fontsize=16, fontweight='bold')
        
        # Ajouter les valeurs
        for bar, val in zip(bars, categorie_counts.values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                    str(val), ha='center', fontweight='bold', fontsize=11)
        
        plt.tight_layout()
        
        if save:
            filename = f'{self.output_dir}/comparaison_casablanca.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ Graphique sauvegardé: {filename}")
        
        plt.show()
    
    def plot_top_villes_vertical(self, n=10, save=True):
        """
        Version verticale du graphique des top villes.
        
        Args:
            n (int): Nombre de villes à afficher
            save (bool): Sauvegarder l'image
        """
        top_villes = self.df['ville'].value_counts().head(n)
        
        fig, ax = plt.subplots(figsize=(14, 7))
        colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(top_villes)))
        
        bars = ax.bar(range(len(top_villes)), top_villes.values, 
                     color=colors, edgecolor='navy', linewidth=0.5)
        
        ax.set_xticks(range(len(top_villes)))
        ax.set_xticklabels(top_villes.index, rotation=45, ha='right', fontsize=11)
        ax.set_ylabel('Nombre d\'offres', fontsize=13, fontweight='bold')
        ax.set_title(f'Top {n} des Villes qui Recrutent - Vue Verticale', 
                    fontsize=18, fontweight='bold', pad=20)
        
        # Ajouter les valeurs
        total = len(self.df)
        for bar, val in zip(bars, top_villes.values):
            pourcentage = (val / total) * 100
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                   f'{val}\n({pourcentage:.1f}%)', 
                   ha='center', fontweight='bold', fontsize=10)
        
        ax.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        
        if save:
            filename = f'{self.output_dir}/top_{n}_villes_vertical.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ Graphique sauvegardé: {filename}")
        
        plt.show()
    
    def plot_heatmap_villes_contrats(self, n_villes=5, n_contrats=5, save=True):
        """
        Crée un heatmap des villes vs types de contrats.
        
        Args:
            n_villes (int): Nombre de villes
            n_contrats (int): Nombre de contrats
            save (bool): Sauvegarder l'image
        """
        top_villes = self.df['ville'].value_counts().head(n_villes).index.tolist()
        top_contrats = self.df['contrat'].value_counts().head(n_contrats).index.tolist()
        
        df_filtered = self.df[
            self.df['ville'].isin(top_villes) & 
            self.df['contrat'].isin(top_contrats)
        ]
        
        pivot_table = pd.crosstab(df_filtered['ville'], df_filtered['contrat'])
        
        if pivot_table.empty:
            print("⚠️ Pas assez de données pour le heatmap")
            return
        
        fig, ax = plt.subplots(figsize=(12, 6))
        im = ax.imshow(pivot_table.values, cmap='YlOrRd', aspect='auto')
        
        # Configuration des axes
        ax.set_xticks(range(len(pivot_table.columns)))
        ax.set_yticks(range(len(pivot_table.index)))
        ax.set_xticklabels(pivot_table.columns, rotation=45, ha='right', fontsize=10)
        ax.set_yticklabels(pivot_table.index, fontsize=10)
        
        # Ajouter les valeurs
        for i in range(len(pivot_table.index)):
            for j in range(len(pivot_table.columns)):
                val = pivot_table.values[i, j]
                color = "white" if val > pivot_table.values.max() / 2 else "black"
                ax.text(j, i, val, ha="center", va="center", 
                       color=color, fontweight='bold')
        
        plt.colorbar(im, ax=ax, label='Nombre d\'offres')
        ax.set_title('Heatmap: Villes vs Types de Contrats', 
                    fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        if save:
            filename = f'{self.output_dir}/heatmap_villes_contrats.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ Graphique sauvegardé: {filename}")
        
        plt.show()
    
    def create_all_ville_plots(self):
        """Crée toutes les visualisations liées aux villes"""
        print("\n🎨 CRÉATION DES VISUALISATIONS SUR LES VILLES")
        print("="*60)
        
        self.plot_top_villes(n=15)
        self.plot_ville_comparison()
        self.plot_top_villes_vertical(n=10)
        self.plot_heatmap_villes_contrats()
        
        print(f"\n✅ Tous les graphiques sauvegardés dans {self.output_dir}/")