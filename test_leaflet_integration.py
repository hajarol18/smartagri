#!/usr/bin/env python3
"""
Script de test pour vérifier l'intégration de la carte Leaflet
Ce script teste la présence et la structure des fichiers nécessaires
"""

import sys
import os

def test_leaflet_files():
    print("🗺️ Test des fichiers Leaflet...")
    required_files = [
        'smart_agri_decision/static/src/js/leaflet_map.js',
        'smart_agri_decision/static/src/css/leaflet_map.css',
        'smart_agri_decision/static/src/xml/leaflet_map.xml',
        'smart_agri_decision/static/src/assets.xml',
        'smart_agri_decision/static/description/index.html'
    ]
    
    missing_files = [file_path for file_path in required_files if not os.path.exists(file_path)]
    if missing_files:
        print(f"❌ Fichiers Leaflet manquants : {missing_files}")
        return False
    else:
        print("✅ Tous les fichiers Leaflet sont présents")
        return True

def test_leaflet_js_content():
    print("\n🔍 Test du contenu JavaScript...")
    js_file = 'smart_agri_decision/static/src/js/leaflet_map.js'
    try:
        with open(js_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_elements = [
            'LeafletMapWidget',
            'AbstractField',
            'fieldRegistry',
            'L.map',
            'L.tileLayer',
            'L.polygon',
            '_startDrawing',
            '_finishDrawing'
        ]
        
        missing_elements = [element for element in required_elements if element not in content]
        if missing_elements:
            print(f"❌ Éléments JavaScript manquants : {missing_elements}")
            return False
        else:
            print("✅ Code JavaScript Leaflet complet")
            return True
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier JS : {e}")
        return False

def test_leaflet_css_content():
    print("\n🎨 Test du contenu CSS...")
    css_file = 'smart_agri_decision/static/src/css/leaflet_map.css'
    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_elements = [
            '.o_leaflet_map_widget',
            '.leaflet-map',
            '.leaflet-draw-control',
            '.leaflet-draw-buttons',
            '#start-drawing',
            '#finish-drawing'
        ]
        
        missing_elements = [element for element in required_elements if element not in content]
        if missing_elements:
            print(f"❌ Éléments CSS manquants : {missing_elements}")
            return False
        else:
            print("✅ Styles CSS Leaflet complets")
            return True
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier CSS : {e}")
        return False

def test_leaflet_xml_content():
    print("\n📋 Test du contenu XML...")
    xml_file = 'smart_agri_decision/static/src/xml/leaflet_map.xml'
    try:
        with open(xml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_elements = [
            'LeafletMapWidget',
            'leaflet-map',
            'o_leaflet_map_widget',
            'Instructions:'
        ]
        
        missing_elements = [element for element in required_elements if element not in content]
        if missing_elements:
            print(f"❌ Éléments XML manquants : {missing_elements}")
            return False
        else:
            print("✅ Template XML Leaflet complet")
            return True
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier XML : {e}")
        return False

def test_assets_integration():
    print("\n🔗 Test de l'intégration des assets...")
    assets_file = 'smart_agri_decision/static/src/assets.xml'
    try:
        with open(assets_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_elements = [
            'assets_backend',
            'leaflet_map.js',
            'leaflet_map.css',
            'leaflet_map_template',
            'unpkg.com/leaflet'
        ]
        
        missing_elements = [element for element in required_elements if element not in content]
        if missing_elements:
            print(f"❌ Éléments d'assets manquants : {missing_elements}")
            return False
        else:
            print("✅ Intégration des assets Leaflet correcte")
            return True
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier assets : {e}")
        return False

def test_manifest_integration():
    print("\n📦 Test de l'intégration dans le manifest...")
    manifest_file = 'smart_agri_decision/__manifest__.py'
    try:
        with open(manifest_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_elements = [
            'static/src/assets.xml',
            'demo_parcelles.xml',
            'leaflet_map.css',
            'leaflet_map.js',
            'leaflet_map.xml'
        ]
        
        missing_elements = [element for element in required_elements if element not in content]
        if missing_elements:
            print(f"❌ Éléments du manifest manquants : {missing_elements}")
            return False
        else:
            print("✅ Manifest mis à jour avec Leaflet")
            return True
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du manifest : {e}")
        return False

def test_parcelle_model():
    print("\n🏗️ Test du modèle parcelle...")
    parcelle_file = 'smart_agri_decision/models/parcelle.py'
    try:
        with open(parcelle_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_elements = [
            'carte_parcelle',
            'geometrie_parcelle',
            'surface_calculee',
            'action_calculer_surface',
            'action_centrer_carte',
            '_calculer_aire_polygone'
        ]
        
        missing_elements = [element for element in required_elements if element not in content]
        if missing_elements:
            print(f"❌ Éléments du modèle parcelle manquants : {missing_elements}")
            return False
        else:
            print("✅ Modèle parcelle avec support Leaflet")
            return True
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du modèle parcelle : {e}")
        return False

def test_parcelle_views():
    print("\n👁️ Test des vues parcelle...")
    views_file = 'smart_agri_decision/views/parcelle_views.xml'
    try:
        with open(views_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_elements = [
            'view_parcelle_agri_form_map',
            'widget="leaflet_map"',
            'Carte Interactive',
            'action_parcelle_agri_map'
        ]
        
        missing_elements = [element for element in required_elements if element not in content]
        if missing_elements:
            print(f"❌ Éléments des vues parcelle manquants : {missing_elements}")
            return False
        else:
            print("✅ Vues parcelle avec carte Leaflet")
            return True
    except Exception as e:
        print(f"❌ Erreur lors de la lecture des vues parcelle : {e}")
        return False

def main():
    print("🚀 Test de l'intégration Leaflet dans Smart Agri Decision")
    print("=" * 60)
    
    tests = [
        test_leaflet_files,
        test_leaflet_js_content,
        test_leaflet_css_content,
        test_leaflet_xml_content,
        test_assets_integration,
        test_manifest_integration,
        test_parcelle_model,
        test_parcelle_views
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur lors du test {test.__name__} : {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS LEAFLET")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        test_name = test.__name__.replace('test_', '').replace('_', ' ').title()
        print(f"{i+1:2d}. {test_name:35s} : {status}")
    
    print(f"\nRésultat global : {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 Tous les tests Leaflet sont passés !")
        print("🗺️ La carte interactive est prête à être utilisée.")
        print("\n📋 Prochaines étapes :")
        print("   1. Redémarrer Odoo pour charger les assets")
        print("   2. Aller dans Agriculture > Gestion des Exploitations > 🗺️ Créer Parcelle (Carte)")
        print("   3. Utiliser les outils de dessin pour créer des parcelles")
        return 0
    else:
        print("\n⚠️  Certains tests ont échoué. Vérifiez l'intégration Leaflet.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
