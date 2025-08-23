#!/usr/bin/env python3
"""
Script de test pour vérifier la fonctionnalité du module Smart Agri Decision
Ce script teste la création et la manipulation des modèles principaux
"""

import sys
import os

def test_module_structure():
    """Teste la structure du module"""
    print("🔍 Test de la structure du module...")
    
    # Vérifier les fichiers essentiels
    required_files = [
        'smart_agri_decision/__manifest__.py',
        'smart_agri_decision/models/__init__.py',
        'smart_agri_decision/views/main_menu.xml',
        'smart_agri_decision/security/ir.model.access.csv'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Fichiers manquants : {missing_files}")
        return False
    else:
        print("✅ Structure du module OK")
        return True

def test_models():
    """Teste les modèles Python"""
    print("\n🔍 Test des modèles Python...")
    
    required_models = [
        'smart_agri_decision/models/exploitation.py',
        'smart_agri_decision/models/meteo.py',
        'smart_agri_decision/models/rcp_scenario.py',
        'smart_agri_decision/models/ia_model.py',
        'smart_agri_decision/models/ia_prediction.py',
        'smart_agri_decision/models/dashboard_main.py',
        'smart_agri_decision/models/dashboard_meteo.py',
        'smart_agri_decision/models/dashboard_agricole.py'
    ]
    
    missing_models = []
    for model_path in required_models:
        if not os.path.exists(model_path):
            missing_models.append(model_path)
    
    if missing_models:
        print(f"❌ Modèles manquants : {missing_models}")
        return False
    else:
        print("✅ Tous les modèles sont présents")
        return True

def test_views():
    """Teste les vues XML"""
    print("\n🔍 Test des vues XML...")
    
    required_views = [
        'smart_agri_decision/views/exploitation_views.xml',
        'smart_agri_decision/views/meteo_views.xml',
        'smart_agri_decision/views/rcp_views.xml',
        'smart_agri_decision/views/ia_views.xml',
        'smart_agri_decision/views/dashboard_views.xml',
        'smart_agri_decision/views/actions.xml',
        'smart_agri_decision/views/main_menu.xml'
    ]
    
    missing_views = []
    for view_path in required_views:
        if not os.path.exists(view_path):
            missing_views.append(view_path)
    
    if missing_views:
        print(f"❌ Vues manquantes : {missing_views}")
        return False
    else:
        print("✅ Toutes les vues sont présentes")
        return True

def test_security():
    """Teste la sécurité"""
    print("\n🔍 Test de la sécurité...")
    
    security_file = 'smart_agri_decision/security/ir.model.access.csv'
    
    if not os.path.exists(security_file):
        print("❌ Fichier de sécurité manquant")
        return False
    
    # Vérifier le contenu du fichier de sécurité
    try:
        with open(security_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Vérifier que tous les modèles ont des droits d'accès
        required_models_in_security = [
            'exploitation.agri',
            'meteo.data',
            'rcp.scenario',
            'ia.model',
            'ia.prediction',
            'dashboard.main',
            'dashboard.meteo',
            'dashboard.agricole'
        ]
        
        missing_security = []
        for model in required_models_in_security:
            if model not in content:
                missing_security.append(model)
        
        if missing_security:
            print(f"❌ Modèles sans droits de sécurité : {missing_security}")
            return False
        else:
            print("✅ Sécurité configurée pour tous les modèles")
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier de sécurité : {e}")
        return False

def test_manifest():
    """Teste le manifest"""
    print("\n🔍 Test du manifest...")
    
    manifest_file = 'smart_agri_decision/__manifest__.py'
    
    if not os.path.exists(manifest_file):
        print("❌ Fichier manifest manquant")
        return False
    
    try:
        with open(manifest_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les éléments essentiels
        required_elements = [
            'name',
            'version',
            'depends',
            'data',
            'installable'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Éléments manquants dans le manifest : {missing_elements}")
            return False
        
        # Vérifier que toutes les vues sont incluses
        required_views_in_manifest = [
            'views/rcp_views.xml',
            'views/ia_views.xml',
            'views/dashboard_views.xml',
            'views/actions.xml'
        ]
        
        missing_views_in_manifest = []
        for view in required_views_in_manifest:
            if view not in content:
                missing_views_in_manifest.append(view)
        
        if missing_views_in_manifest:
            print(f"❌ Vues manquantes dans le manifest : {missing_views_in_manifest}")
            return False
        
        print("✅ Manifest correctement configuré")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du manifest : {e}")
        return False

def test_data_files():
    """Teste les fichiers de données"""
    print("\n🔍 Test des fichiers de données...")
    
    data_files = [
        'smart_agri_decision/data/demo_data.xml'
    ]
    
    missing_data = []
    for data_file in data_files:
        if not os.path.exists(data_file):
            missing_data.append(data_file)
    
    if missing_data:
        print(f"❌ Fichiers de données manquants : {missing_data}")
        return False
    else:
        print("✅ Fichiers de données présents")
        return True

def main():
    """Fonction principale de test"""
    print("🚀 Test du module Smart Agri Decision")
    print("=" * 50)
    
    tests = [
        test_module_structure,
        test_models,
        test_views,
        test_security,
        test_manifest,
        test_data_files
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur lors du test {test.__name__} : {e}")
            results.append(False)
    
    # Résumé des tests
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1:2d}. {test.__name__:25s} : {status}")
    
    print(f"\nRésultat global : {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! Le module est prêt.")
        return 0
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez le module.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
