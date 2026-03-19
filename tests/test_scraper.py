"""Tests unitaires pour le scraper"""

import pytest
import sys
import os
from unittest.mock import Mock, patch
import requests

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
        # Mock de la réponse requests
        with patch('requests.Session.get') as mock_get:
            # Créer une réponse mock
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = '''
            <html>
                <div class="card-job" data-href="/offre-emploi-maroc/test-1">Offre 1</div>
                <div class="card-job" data-href="/offre-emploi-maroc/test-2">Offre 2</div>
            </html>
            '''
            mock_get.return_value = mock_response
            
            urls = self.scraper.get_page_urls(0)
            assert isinstance(urls, list)
            assert len(urls) == 2
            assert "test-1" in urls[0]
    
    def test_parse_job(self):
        # Mock de la réponse requests
        with patch('requests.Session.get') as mock_get:
            # Simuler une réponse HTML d'une offre
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = '''
            <html>
                <h1 class="text-center">Responsable Commercial - Casablanca</h1>
                <a href="/recruteur/123">Entreprise Test</a>
                <p>Publiée le 19.03.2026</p>
                <li class="withicon location-dot"><span>Casablanca-Mohammedia</span></li>
                <div class="card-block-summary">
                    <li>Contrat proposé : <span>CDI</span></li>
                    <li>Expérience : <span>5 ans</span></li>
                    <li>Niveau d'études : <span>Bac+5</span></li>
                </div>
                <ul class="skills">
                    <li>Python</li>
                    <li>Pandas</li>
                </ul>
            </html>
            '''
            mock_get.return_value = mock_response
            
            job = self.scraper.parse_job("https://test.com")
            assert job is not None
            assert job['titre'] == "Responsable Commercial - Casablanca"
            assert job['entreprise'] == "Entreprise Test"
            assert job['date_publication'] == "19.03.2026"
            assert job['region'] == "Casablanca-Mohammedia"
            assert job['contrat'] == "CDI"
            assert job['experience'] == "5 ans"
            assert job['niveau_etude'] == "Bac+5"
            assert "Python" in job['competences_cles']