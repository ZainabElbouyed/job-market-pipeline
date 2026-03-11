"""Configuration des styles de visualisation"""

import matplotlib.pyplot as plt
import seaborn as sns

def configure_styles():
    """Configure les styles globaux pour les visualisations"""
    
    # Style de base
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    
    # Configuration des polices
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.titlesize'] = 18
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['axes.labelsize'] = 13
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['xtick.labelsize'] = 11
    plt.rcParams['ytick.labelsize'] = 11
    plt.rcParams['legend.fontsize'] = 11
    
    # Configuration des couleurs
    plt.rcParams['axes.edgecolor'] = 'navy'
    plt.rcParams['axes.linewidth'] = 0.5
    plt.rcParams['grid.alpha'] = 0.3
    
    print("✅ Styles de visualisation configurés")

def get_color_gradient(n_colors, cmap='viridis'):
    """
    Génère un gradient de couleurs.
    
    Args:
        n_colors (int): Nombre de couleurs
        cmap (str): Nom du colormap
        
    Returns:
        list: Liste de couleurs
    """
    import numpy as np
    import matplotlib.pyplot as plt
    
    cmap = plt.cm.get_cmap(cmap)
    return [cmap(i) for i in np.linspace(0.2, 0.9, n_colors)]