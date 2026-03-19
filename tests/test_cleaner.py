"""Tests pour le module de nettoyage"""

import pytest
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.cleaner import DataCleaner

class TestCleaner:
    
    def setup_method(self):
        self.cleaner = DataCleaner()
        self.test_df = pd.DataFrame({
            'titre': ['Offre 1', 'Offre 2'],
            'entreprise': ['Société A', None],
            'ville': ['Casablanca ', ' '],
            'url': ['url1', 'url1']  # Doublon
        })
    
    def test_clean(self):
        df_clean = self.cleaner.clean(self.test_df)
        assert len(df_clean) == 1  # Doublon supprimé
        assert df_clean['ville'].iloc[0] == 'Casablanca'
        assert df_clean['entreprise'].iloc[0] == 'Société A'