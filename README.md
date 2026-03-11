# 🚀 Job Market Pipeline - Analyse du Marché de l'Emploi au Maroc

---

## 📋 Table des matières
- [Description](#-description)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Technologies](#-technologies)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Résultats](#-résultats)
- [Structure du projet](#-structure-du-projet)
- [Contribution](#-contribution)

---

## 🎯 Description

**Job Market Pipeline** est un projet complet d'analyse du marché de l'emploi au Maroc. Il automatise la collecte, le nettoyage, l'analyse et la visualisation de **700+ offres d'emploi** provenant du site Emploi.ma.

L'objectif est d'identifier les **tendances du marché** et les **compétences les plus demandées** pour aider les chercheurs d'emploi et les recruteurs à prendre des décisions éclairées.

---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|----------------|-------------|
| **🕷️ Web Scraping** | Collecte automatisée de 700+ offres avec Requests et BeautifulSoup |
| **🧹 Pipeline ETL** | Nettoyage, transformation et standardisation des données avec Pandas |
| **📊 Analyse statistique** | Identification des top compétences, régions, types de contrats |
| **🎨 Visualisation** | Graphiques professionnels avec Matplotlib, Seaborn et WordCloud |
| **🤖 Automatisation** | Scripts planifiables pour des collectes régulières |
| **📓 Notebooks Jupyter** | Démonstrations interactives de chaque étape |

---

## 🏗 Architecture

```mermaid
graph LR
    S[("🌐 Emploi.ma")] --> E[📤 Extraction]
    E --> T[🔄 Transformation]
    T --> A[📊 Analyse]
    A --> V[🎨 Visualisation]
    
    subgraph E [Extraction]
        E1[Requests] --> E2[BeautifulSoup]
    end
    
    subgraph T [Transformation]
        T1[Nettoyage] --> T2[Standardisation]
    end
    
    subgraph A [Analyse]
        A1[Stats] --> A2[Tendances]
    end
    
    subgraph V [Visualisation]
        V1[Matplotlib] --> V2[Seaborn]
    end
```

---

## 🛠 Technologies

### **Langages & Bibliothèques**
| Technologie | Utilisation |
|-------------|-------------|
| **Python 3.8+** | Langage principal |
| **Requests** | Requêtes HTTP |
| **BeautifulSoup4** | Parsing HTML |
| **Pandas** | Manipulation et analyse de données |
| **NumPy** | Calculs numériques |
| **Matplotlib** | Visualisations de base |
| **Seaborn** | Visualisations avancées |
| **WordCloud** | Nuages de mots |
| **Schedule** | Automatisation des tâches |

### **Outils de développement**
- **Jupyter Notebook** : Exploration interactive
- **Git** : Versionnement
- **Pytest** : Tests unitaires

---

## 📦 Installation

### **1. Cloner le repository**
```bash
git clone https://github.com/ZainabElbouyed/job-market-pipeline.git
cd job-market-pipeline
```

### **2. Créer un environnement virtuel**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### **3. Installer les dépendances**
```bash
pip install -r requirements.txt
```

---

## 🚀 Utilisation

### **1. Scraping seul (collecte des données)**
```bash
python scripts/run_scraper.py --pages 30
```

### **2. Pipeline complet (scraping + analyse + visualisation)**
```bash
python scripts/run_pipeline.py --pages 30 --visuals
```

### **3. Analyse avec données existantes**
```bash
python scripts/run_pipeline.py --no-scrape --visuals
```

### **4. Exploration interactive avec Jupyter**
```bash
jupyter notebook
# Ouvre ensuite notebooks/01_scraping.ipynb
```

### **5. Automatisation (exécution programmée)**
```bash
# Exécution quotidienne à 9h
python scripts/scheduler.py --daily --time "09:00"

# Exécution toutes les 6 heures
python scripts/scheduler.py --interval 21600
```

---

## 📊 Résultats

### **Données générées**
| Dossier | Contenu |
|---------|---------|
| `data/raw/` | Fichiers CSV bruts (jobs_YYYYMMDD.csv) |
| `data/processed/` | Données nettoyées et transformées |
| `analysis/reports/` | Rapports statistiques (.txt) |
| `visualization/outputs/` | Graphiques PNG |

### **Exemples de visualisations**
- **Top 20 des compétences** les plus demandées
- **Top 15 des villes** qui recrutent
- **Répartition des types de contrats** (CDI, CDD, Intérim...)
- **Nuage de mots** des intitulés de poste
- **Heatmap** compétences par région

---

## 📁 Structure du projet

```
job-market-pipeline/
│
├── 📂 data/                           # Données brutes et traitées
│   ├── raw/                           # Données scraping originales
│   │   └── jobs_YYYYMMDD_HHMMSS.csv
│   └── processed/                      # Données nettoyées
│       └── jobs_clean.csv
│
├── 📂 scraper/                         # Module de collecte
│   ├── __init__.py
│   ├── config.py                       # URLs, headers, constantes
│   ├── utils.py                         # Fonctions helpers (extract_city, etc.)
│   ├── scraper.py                       # Classes/fonctions principales
│   └── scraper.ipynb                     # Démo et tests du scraper
│
├── 📂 pipeline/                          # Pipeline ETL
│   ├── __init__.py
│   ├── cleaner.py                        # Nettoyage des données
│   ├── transformer.py                     # Transformation (compétences, etc.)
│   └── pipeline.ipynb                      # Orchestration du pipeline
│
├── 📂 analysis/                           # Analyse statistique
│   ├── __init__.py
│   ├── stats.py                            # Fonctions d'analyse
│   ├── reports.py                           # Génération de rapports
│   └── analysis.ipynb                        # Exploration des données
│
├── 📂 visualization/                       # Graphiques
│   ├── __init__.py
│   ├── plots.py                              # Fonctions de visualisation
│   ├── styles.py                              # Configuration des styles
│   ├── outputs/                                # Images sauvegardées
│   └── plots.ipynb                             # Démo des visualisations
│
├── 📂 notebooks/                         # Notebooks de démonstration
│   ├── outputs/                          # Images sauvegardées
│   ├── 01_scraping.ipynb
│   ├── 02_pipeline.ipynb
│   ├── 03_analysis.ipynb
│   └── 04_visualization.ipynb
│
├── 📂 scripts/                             # Scripts d'automatisation
│   ├── run_scraper.py                        # Scraping programmé
│   ├── run_pipeline.py                        # Pipeline complet
│   └── scheduler.py                           # Planification cron/airflow
│
├── 📂 tests/                                # Tests unitaires
│   ├── test_scraper.py
│   ├── test_cleaner.py
│   └── test_analysis.py
│
├── 📄 requirements.txt                      # Dépendances
├── 📄 .gitignore                              # Fichiers à ignorer
└── 📄 README.md                               # Documentation
 
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le projet
2. Crée ta branche (`git checkout -b feature/ma-feature`)
3. **Commit** tes changements (`git commit -m 'Ajout de ma feature'`)
4. **Push** vers la branche (`git push origin feature/ma-feature`)
5. Ouvre une **Pull Request**

---

## ✨ Auteur

**Zainab EL BOUYED** - [GitHub](https://github.com/ZainabElbouyed) - [LinkedIn](https://www.linkedin.com/in/zainab-el-bouyed-85700535b/))

---

⭐ **Si ce projet t'a aidé, n'hésite pas à lui mettre une étoile !** ⭐
