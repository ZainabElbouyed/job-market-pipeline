"""Fonctions utilitaires pour le scraping"""

import re
from .config import MAROC_CITIES

def extract_city_from_title(title):
    """
    Extrait la ville depuis le titre de l'offre.
    
    Args:
        title (str): Titre de l'offre
        
    Returns:
        str: Ville extraite ou None
    """
    if not title:
        return None
    
    patterns = [
        r'-\s*([A-Za-zéèêëàâîïôûç\s-]+?)(?:\s*\(|,|\s*$)',
        r'à\s*([A-Za-zéèêëàâîïôûç\s-]+?)(?:\s*\(|,|\s*$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            city_candidate = match.group(1).strip()
            for city in MAROC_CITIES:
                if city.lower() in city_candidate.lower():
                    return city
            return city_candidate
    return None

def clean_text(text):
    """Nettoie le texte (espaces, sauts de ligne)"""
    if not text:
        return None
    return ' '.join(text.split())

def extract_number(text):
    """Extrait un nombre depuis un texte"""
    if not text:
        return None
    match = re.search(r'\d+', text)
    return int(match.group()) if match else None