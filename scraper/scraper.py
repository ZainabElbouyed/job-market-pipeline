"""Module principal de scraping"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
import logging
from urllib.parse import urljoin
from datetime import datetime

from .config import BASE_URL, SEARCH_URL, HEADERS, DELAY
from .utils import extract_city_from_title, clean_text

logger = logging.getLogger(__name__)

class EmploiMaScraper:
    """Scraper pour le site Emploi.ma"""
    
    def __init__(self, delay=DELAY):
        self.base_url = BASE_URL
        self.search_url = SEARCH_URL
        self.headers = HEADERS
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
    def get_page_urls(self, page_num=0):
        """
        Récupère les URLs des offres sur une page de recherche.
        
        Args:
            page_num (int): Numéro de page
            
        Returns:
            list: Liste des URLs d'offres
        """
        url = f"{self.search_url}?page={page_num}"
        
        try:
            time.sleep(random.uniform(2,4))
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            urls = []
            for card in soup.find_all('div', class_='card-job'):
                link = card.get('data-href')
                if link:
                    full_url = urljoin(self.base_url, link)
                    urls.append(full_url)
            
            return urls
            
        except requests.RequestException as e:
            logger.error(f"Erreur page {page_num}: {e}")
            return []
    
    def parse_job(self, url):
        """
        Parse une offre d'emploi individuelle.
        
        Args:
            url (str): URL de l'offre
            
        Returns:
            dict: Données extraites
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            job = {
                'url': url,
                'titre': None,
                'entreprise': None,
                'date_publication': None,
                'region': None,
                'ville': None,
                'contrat': None,
                'experience': None,
                'niveau_etude': None,
                'competences_cles': None
            }
            
            # Titre
            title_tag = soup.find('h1', class_='text-center')
            if title_tag:
                job['titre'] = clean_text(title_tag.text)
                job['ville'] = extract_city_from_title(job['titre'])
            
            # Entreprise
            company_tag = soup.find('a', href=re.compile(r'/recruteur/\d+'))
            if company_tag:
                job['entreprise'] = clean_text(company_tag.text)
            else:
                nc_element = soup.find(string=re.compile(r'N\.C\.|Confidentiel'))
                job['entreprise'] = 'Confidentiel' if nc_element else 'Non spécifié'
            
            # Date
            date_tag = soup.find('p', string=re.compile(r'Publiée le'))
            if date_tag:
                date_text = date_tag.text
                job['date_publication'] = re.sub(r'Publiée le\s*', '', date_text).strip()
            
            # Région
            region_li = soup.find('li', class_='withicon location-dot')
            if region_li and region_li.find('span'):
                job['region'] = clean_text(region_li.find('span').text)
            
            # Informations du résumé
            summary = soup.find('div', class_='card-block-summary')
            if summary:
                for item in summary.find_all('li'):
                    text = item.text
                    span = item.find('span')
                    if span:
                        if re.search(r'CDI|CDD|Freelance|Stage|Intérim|Anapec', text):
                            job['contrat'] = clean_text(span.text)
                        elif 'Expérience' in text:
                            job['experience'] = clean_text(span.text)
                        elif 'Bac' in text or 'Niveau' in text:
                            job['niveau_etude'] = clean_text(span.text)
            
            # Compétences
            skills_ul = soup.find('ul', class_='skills')
            if skills_ul:
                skills = []
                for li in skills_ul.find_all('li'):
                    skill = clean_text(li.text)
                    if skill:
                        skills.append(skill)
                job['competences_cles'] = ' - '.join(skills)
            
            return job
            
        except Exception as e:
            logger.error(f"Erreur parsing {url}: {e}")
            return None
    
    def get_all_urls(self, max_pages=30):
        """
        Collecte les URLs de toutes les pages.
        
        Args:
            max_pages (int): Nombre maximum de pages
            
        Returns:
            list: Toutes les URLs
        """
        all_urls = []
        
        for page in range(max_pages):
            logger.info(f"Page {page+1}/{max_pages}")
            urls = self.get_page_urls(page)
            
            if not urls:
                break
                
            all_urls.extend(urls)
            time.sleep(self.delay + random.uniform(0, 1))
        
        # Supprimer les doublons
        all_urls = list(set(all_urls))
        logger.info(f"Total: {len(all_urls)} URLs trouvées")
        
        return all_urls
    
    def run(self, max_pages=30, sample=None):
        """
        Exécute le scraping complet.
        
        Args:
            max_pages (int): Nombre de pages à scraper
            sample (int): Taille d'échantillon (optionnel)
            
        Returns:
            pd.DataFrame: Données collectées
        """
        start_time = time.time()
        all_jobs = []
        
        # Collecte des URLs
        all_urls = self.get_all_urls(max_pages=max_pages)
        
        # Échantillonnage
        if sample and sample < len(all_urls):
            all_urls = random.sample(all_urls, sample)
            logger.info(f"Échantillon de {sample} offres")
        
        # Parsing
        for i, url in enumerate(all_urls, 1):
            logger.info(f"Parsing {i}/{len(all_urls)}")
            job = self.parse_job(url)
            if job:
                all_jobs.append(job)
            time.sleep(self.delay/2 + random.uniform(0, 0.5))
        
        # Création du DataFrame
        df = pd.DataFrame(all_jobs)
        
        # Sauvegarde
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        import os
        os.makedirs('../data/raw', exist_ok=True)

        df.to_csv(f'../data/raw/jobs_{timestamp}.csv', index=False)
        
        logger.info(f"✅ Scraping terminé: {len(df)} offres")
        logger.info(f"⏱️ Temps: {time.time()-start_time:.2f}s")
        
        return df