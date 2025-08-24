# 🐳 Résolution du Problème Docker - Odoo 18 Internal Server Error

## 📋 Problème Rencontré

**Date** : 2025-01-XX  
**Symptôme** : Erreur "Internal Server Error" lors de l'accès à Odoo via `http://localhost:10018/`  
**Cause** : Configuration Docker incorrecte avec conflits de ports et variables d'environnement

## 🔍 Diagnostic

### 1. Containers en Double
```bash
# Problème : 2 containers Odoo qui tournent en même temps
docker ps -a
# Résultat : Container en état "Created" + Container "Running"
```

### 2. Configuration Docker Compose Incorrecte
```yaml
# ❌ PROBLÉMATIQUE - Variables d'environnement incorrectes
environment:
  - HOST=db                    # Variable non reconnue par Odoo
  - USER=odoo                  # Variable non reconnue par Odoo  
  - PASSWORD=odoo18@2024      # Variable non reconnue par Odoo

# ❌ PROBLÉMATIQUE - 2 ports qui créent des conflits
ports:
  - "10018:8069"              # Port principal
  - "20018:8072"              # Port live chat (conflit)
```

### 3. Erreurs dans le Module
```python
# ❌ PROBLÉMATIQUE - Virgule en trop dans __manifest__.py
"data": [
    "security/ir.model.access.csv",
    "views/exploitation_views.xml",
    # ... autres vues ...
    "data/demo_data.xml",      # ← Virgule en trop ici
],
```

## ✅ Solutions Appliquées

### 1. Correction des Variables d'Environnement
```yaml
# ✅ CORRECT - Variables Odoo standard
environment:
  - ODOO_DATABASE_HOST=db
  - ODOO_DATABASE_USER=odoo
  - ODOO_DATABASE_PASSWORD=odoo18@2024
  - PIP_BREAK_SYSTEM_PACKAGES=1
```

### 2. Simplification des Ports
```yaml
# ✅ CORRECT - Un seul port pour éviter les conflits
ports:
  - "10018:8069"              # Port principal uniquement
```

### 3. Correction du Manifest
```python
# ✅ CORRECT - Suppression de la virgule en trop
"data": [
    "security/ir.model.access.csv",
    "views/exploitation_views.xml",
    # ... autres vues ...
    "data/demo_data.xml"       # ← Plus de virgule
],
```

## 🚀 Procédure de Résolution

### Étape 1 : Nettoyage Complet
```bash
# Arrêter tous les containers
docker-compose down

# Nettoyer les containers orphelins
docker container prune -f
```

### Étape 2 : Correction des Fichiers
1. Modifier `docker-compose.yml` (variables d'environnement + ports)
2. Corriger `__manifest__.py` (virgule en trop)
3. Vérifier la syntaxe

### Étape 3 : Redémarrage Propre
```bash
# Redémarrer avec la configuration corrigée
docker-compose up -d

# Vérifier l'état
docker ps
```

## 📊 Résultat Final

✅ **2 containers actifs** : `odoo18` + `db`  
✅ **1 seul port** : `10018:8069`  
✅ **Variables d'environnement correctes**  
✅ **Module `smart_agri_decision` fonctionnel**  
✅ **Plus d'erreur "Internal Server Error"**  

## 🔧 Configuration Finale Recommandée

```yaml
services:
  db:
    image: postgres:16
    environment:
      - POSTGRES_USER=odoo
      - POSTGRES_PASSWORD=odoo18@2024
      - POSTGRES_DB=postgres
    volumes:
      - ./postgresql:/var/lib/postgresql/data
    restart: always

  odoo18:
    image: odoo:18
    depends_on:
      - db
    ports:
      - "10018:8069"                    # Port principal uniquement
    environment:
      - ODOO_DATABASE_HOST=db           # Variable Odoo standard
      - ODOO_DATABASE_USER=odoo         # Variable Odoo standard
      - ODOO_DATABASE_PASSWORD=odoo18@2024  # Variable Odoo standard
    volumes:
      - ./smartagri:/mnt/extra-addons   # Module smart_agri_decision
      - ./etc:/etc/odoo                 # Configuration Odoo
    restart: always
```

## 🎯 Points Clés à Retenir

1. **Toujours utiliser les variables d'environnement Odoo standard**
2. **Éviter les ports multiples** pour Odoo (sauf si nécessaire)
3. **Vérifier la syntaxe Python** dans les manifests
4. **Nettoyer complètement** avant de redémarrer
5. **Tester progressivement** : d'abord Odoo basique, puis avec modules

## 📚 Ressources

- [Repository GitHub](https://github.com/hajarol18/smartagri.git)
- [Documentation Odoo Docker](https://hub.docker.com/_/odoo)
- [Variables d'environnement Odoo](https://www.odoo.com/documentation/16.0/administration/install/docker.html)

---

**💡 Cette documentation permet à ChatGPT et d'autres développeurs de résoudre rapidement ce type de problème !**
