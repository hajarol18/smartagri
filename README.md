# 🌾 Smart Agri Decision - Module Odoo 18

## 📋 Description

**Smart Agri Decision** est un module Odoo 18 innovant pour l'aide à la décision agricole basé sur les paiements géographiques et l'analyse climatique. Ce module intègre des fonctionnalités avancées de météorologie, de gestion d'exploitations et d'analyse prédictive.

## ✨ Fonctionnalités Principales

### 🌤️ **Module Météorologique (Meteostat)**
- **Import automatique** de données météo sur 7 jours
- **Calcul automatique des alertes** : gel, canicule, sécheresse, inondation, vent
- **Stress hydrique et thermique** calculés automatiquement
- **Interface complète** : données météo, alertes, tendances climatiques

### 🏡 **Gestion des Exploitations**
- **Géolocalisation** avec latitude/longitude
- **Zones climatiques** (Méditerranéen, Océanique, Continental, Montagnard)
- **Types de sol** (Argileux, Limoneux, Sableux, Calcaire, Humifère)
- **Suivi météorologique** intégré

### 📊 **Données Climatiques**
- **Modèle météo.data** complet avec tous les paramètres
- **Vues spécialisées** : listes, formulaires, recherche
- **Filtres intelligents** pour les alertes et tendances
- **Calculs automatiques** des indices de stress

### 🔬 **Modules Avancés (En développement)**
- **Scénarios RCP IPCC** pour la modélisation climatique
- **Modèles IA et prédictions** avec machine learning
- **Intégration API Meteostat** pour données réelles
- **Tableaux de bord interactifs** avec cartes

## 🚀 Installation

### Prérequis
- Odoo 18
- Docker et Docker Compose (recommandé)
- PostgreSQL

### ⚠️ Résolution des Problèmes Docker

Si vous rencontrez l'erreur **"Internal Server Error"** lors de l'installation, consultez :
- [Guide de résolution Docker](DOCKER_ISSUE_RESOLUTION.md) - Solution complète
- [Docker Compose corrigé](docker-compose-corrected.yml) - Configuration de référence

### Installation via Docker
```bash
# Cloner le repository
git clone https://github.com/hajarol18/smartagri.git

# Copier le module dans le dossier addons d'Odoo
cp -r smartagri/smart_agri_decision /path/to/odoo/addons/

# Redémarrer Odoo
docker compose restart odoo18

# Mettre à jour le module
docker compose exec odoo18 odoo -d postgres -u smart_agri_decision --stop-after-init
```

### Installation manuelle
1. Copiez le dossier `smart_agri_decision` dans votre dossier addons Odoo
2. Redémarrez le serveur Odoo
3. Mettez à jour la liste des applications
4. Installez le module "Smart Agri Decision"

## 📁 Structure du Module

```
smart_agri_decision/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── exploitation.py      # Gestion des exploitations
│   ├── meteo.py            # Données météorologiques
│   ├── parcelle.py         # Gestion des parcelles
│   ├── culture.py          # Types de cultures
│   ├── intervention.py     # Interventions agricoles
│   ├── intrants_ressources.py # Ressources et intrants
│   ├── rcp_scenarios.py    # Scénarios climatiques IPCC
│   └── ia_predictions.py   # Prédictions IA
├── views/
│   ├── main_menu.xml       # Menu principal
│   ├── exploitation_views.xml # Vues des exploitations
│   ├── meteo_views.xml     # Vues météorologiques
│   ├── parcelle_views.xml  # Vues des parcelles
│   ├── culture_views.xml   # Vues des cultures
│   ├── intervention_views.xml # Vues des interventions
│   └── intrants_views.xml  # Vues des intrants
├── security/
│   └── ir.model.access.csv # Droits d'accès
└── data/
    └── demo_data.xml       # Données de démonstration
```

## 🎯 Utilisation

### 1. Créer une Exploitation
- Allez dans **"Gestion des Exploitations" → "Exploitations agricoles"**
- Créez une nouvelle exploitation avec :
  - Nom et coordonnées géographiques
  - Zone climatique et type de sol
  - Informations de contact

### 2. Importer les Données Météo
- Ouvrez votre exploitation
- Cliquez sur **"🌤️ Importer Météo (7 jours)"**
- Le système crée automatiquement 7 jours de données simulées
- Les alertes sont calculées automatiquement

### 3. Consulter les Données Climatiques
- **"Données Climatiques" → "Données météo"** : Toutes les données
- **"Données Climatiques" → "Alertes climatiques"** : Alertes actives
- **"Données Climatiques" → "Tendances climatiques"** : Analyses temporelles

## 🔧 Configuration

### Champs Météorologiques
- **Température** (°C) avec min/max
- **Précipitations** (mm) et probabilité
- **Humidité relative** (%)
- **Vitesse et direction du vent**
- **Pression atmosphérique** (hPa)
- **Rayonnement solaire** (W/m²)
- **Évapotranspiration** (mm)

### Seuils d'Alerte
- **Gel** : Température < 0°C
- **Canicule** : Température > 35°C
- **Sécheresse** : Précipitations < 1mm
- **Inondation** : Précipitations > 50mm
- **Vent fort** : Vitesse > 50 km/h

## 🚧 Développement

### Prochaines Étapes
1. **Intégration API Meteostat** pour données réelles
2. **Modèles de machine learning** pour prédictions
3. **Scénarios RCP IPCC** complets
4. **Tableaux de bord** avec cartes interactives
5. **API REST** pour intégrations externes

### Contribution
Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Contribuer au code
- Améliorer la documentation

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 👨‍💻 Auteur

**Hajar** - Développeur du module Smart Agri Decision

## 🌟 Remerciements

- **Odoo Community** pour le framework
- **Meteostat** pour l'inspiration des données météo
- **GitHub** pour l'hébergement du code

---

**🌾 Smart Agri Decision - L'avenir de l'agriculture intelligente commence ici !**
