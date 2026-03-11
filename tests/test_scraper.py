"""Tests unitaires pour le scraper"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.scraper import EmploiMaScraper
from scraper.utils import extract_city_from_title

class TestScraper:
    
    def setup_method(self):
        self.scraper = EmploiMaScraper()
    
    def test_extract_city(self):
        assert extract_city_from_title("Commercial - Casablanca") == "Casablanca"
        assert extract_city_from_title("Ingénieur à Rabat") == "Rabat"
        assert extract_city_from_title("Manager Tanger") is None
    
    def test_get_page_urls(self):
        urls = self.scraper.get_page_urls(0)
        assert isinstance(urls, list)
    
    def test_parse_job(self):
        # Test avec une URL de démonstration
        url = "https://www.emploi.ma/offre-emploi-maroc/responsable-commercial-designer-casablanca-9265950"
        job = self.scraper.parse_job(url)
        assert job is not None
        assert 'titre' in job