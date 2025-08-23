# 🚀 Guide de Déploiement - Smart Agri Decision

## 📋 Prérequis

### Système
- **OS** : Windows 10/11, macOS, ou Linux
- **RAM** : Minimum 8GB (recommandé 16GB)
- **Stockage** : Minimum 10GB d'espace libre
- **Docker** : Version 20.10 ou supérieure

### Logiciels
- **Docker Desktop** : [Télécharger ici](https://www.docker.com/products/docker-desktop)
- **Git** : [Télécharger ici](https://git-scm.com/downloads)
- **Navigateur web** : Chrome, Firefox, Edge, ou Safari

## 🎯 Installation Rapide

### 1. **Cloner le Repository**
```bash
git clone https://github.com/hajarol18/smartagri.git
cd smartagri
```

### 2. **Démarrage Automatique**

#### Sur Windows (PowerShell)
```powershell
.\install.ps1
```

#### Sur Linux/macOS
```bash
chmod +x install.sh
./install.sh
```

### 3. **Accès à l'Application**
- **Odoo** : http://localhost:10018
- **PgAdmin** : http://localhost:5050

## 🔧 Installation Manuelle

### Étape 1 : Vérifier Docker
```bash
docker --version
docker-compose --version
```

### Étape 2 : Démarrer les Services
```bash
docker-compose up -d
```

### Étape 3 : Vérifier le Démarrage
```bash
docker-compose ps
docker-compose logs odoo18
```

### Étape 4 : Mettre à Jour le Module
```bash
docker-compose exec odoo18 odoo -d smartagri -u smart_agri_decision --stop-after-init
```

## 🌐 Configuration

### Variables d'Environnement
```bash
# Base de données
POSTGRES_DB=smartagri
POSTGRES_USER=odoo
POSTGRES_PASSWORD=odoo

# Odoo
ODOO_PORT=10018
ODOO_DEV_MODE=true
```

### Ports Utilisés
- **10018** : Odoo (interface principale)
- **5432** : PostgreSQL (base de données)
- **5050** : PgAdmin (administration DB)

## 🧪 Tests

### Tests Automatiques
```bash
# Lancer les tests
python -m pytest tests/

# Tests avec couverture
python -m pytest tests/ --cov=smart_agri_decision

# Tests spécifiques
python -m pytest tests/test_meteo.py -v
```

### Tests Manuels
1. **Créer une exploitation** avec coordonnées
2. **Importer des données météo** (7 jours)
3. **Vérifier les alertes** automatiques
4. **Consulter les données** dans les menus climatiques

## 🔍 Dépannage

### Problèmes Courants

#### Odoo ne démarre pas
```bash
# Vérifier les logs
docker-compose logs odoo18

# Redémarrer le service
docker-compose restart odoo18

# Vérifier l'espace disque
docker system df
```

#### Erreur de base de données
```bash
# Redémarrer PostgreSQL
docker-compose restart postgres

# Vérifier la connexion
docker-compose exec postgres psql -U odoo -d smartagri
```

#### Module non trouvé
```bash
# Vérifier le chemin des addons
docker-compose exec odoo18 ls -la /mnt/extra-addons/

# Mettre à jour la liste des modules
docker-compose exec odoo18 odoo -d smartagri --update=smart_agri_decision
```

### Logs et Monitoring
```bash
# Logs en temps réel
docker-compose logs -f odoo18

# Logs PostgreSQL
docker-compose logs -f postgres

# Utilisation des ressources
docker stats
```

## 📊 Performance

### Optimisations Recommandées
- **Workers Odoo** : 2-4 selon la RAM disponible
- **Cache PostgreSQL** : Augmenter si possible
- **Volumes** : Utiliser des volumes nommés pour la persistance

### Monitoring
```bash
# Utilisation CPU/RAM
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Espace disque
docker system df -v

# Logs de performance
docker-compose exec odoo18 tail -f /var/log/odoo/odoo.log
```

## 🔒 Sécurité

### Bonnes Pratiques
- **Changer les mots de passe** par défaut
- **Limiter l'accès réseau** si nécessaire
- **Mettre à jour régulièrement** les images Docker
- **Sauvegarder** régulièrement la base de données

### Sauvegarde
```bash
# Sauvegarde de la base
docker-compose exec postgres pg_dump -U odoo smartagri > backup_$(date +%Y%m%d_%H%M%S).sql

# Sauvegarde des volumes
docker run --rm -v smartagri_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .
```

## 🚀 Déploiement en Production

### Environnement de Production
- **Reverse Proxy** : Nginx ou Apache
- **SSL/TLS** : Certificats Let's Encrypt
- **Monitoring** : Prometheus + Grafana
- **Backup** : Automatisé avec cron

### Docker Compose Production
```yaml
version: '3.8'
services:
  odoo18:
    restart: always
    environment:
      - ODOO_DEV_MODE=false
    volumes:
      - ./odoo.conf:/etc/odoo/odoo.conf
```

## 📞 Support

### Ressources
- **Documentation** : [README.md](README.md)
- **Issues** : [GitHub Issues](https://github.com/hajarol18/smartagri/issues)
- **Wiki** : [Documentation détaillée](https://github.com/hajarol18/smartagri/wiki)

### Contact
- **Auteur** : Hajar
- **Repository** : https://github.com/hajarol18/smartagri
- **Email** : hajar@example.com

---

**🌾 Smart Agri Decision - Déploiement simplifié pour l'agriculture intelligente !**
