"""Configuration du scraper"""

BASE_URL = "https://www.emploi.ma"
SEARCH_URL = "https://www.emploi.ma/recherche-jobs-maroc"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.google.com/"
}


# Augmenter le délai
DELAY = 5

# Timeout plus long
TIMEOUT = 30

# Utiliser un vrai navigateur comme référence
REFERER = "https://www.google.com/"

# Villes marocaines pour l'extraction
MAROC_CITIES = [
    'Casablanca', 'Rabat', 'Fès', 'Marrakech', 'Tanger', 'Agadir', 'Meknès',
    'Oujda', 'Kénitra', 'Tétouan', 'Safi', 'Mohammedia', 'El Jadida', 'Nador',
    'Beni Mellal', 'Khouribga', 'Settat', 'Larache', 'Taza', 'Guelmim',
    'Dakhla', 'Laâyoune', 'Témara', 'Salé', 'Bouskoura', 'Aïn Harrouda'
]