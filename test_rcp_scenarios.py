#!/usr/bin/env python3
"""
Test des Scénarios RCP IPCC dans Smart Agri Decision
Vérifie la génération automatique et l'analyse des scénarios
"""

import os
import sys
import xml.etree.ElementTree as ET

def test_rcp_menu_structure():
    """Test de la structure du menu RCP"""
    print("🔍 Test de la structure du menu RCP...")
    
    try:
        tree = ET.parse('smart_agri_decision/views/main_menu.xml')
        root = tree.getroot()
        
        # Vérifier la présence du menu climatique
        climat_menu = root.find(".//menuitem[@id='menu_climat_main']")
        if climat_menu is None:
            print("❌ Menu climatique manquant")
            return False
        
        # Vérifier la présence du sous-menu RCP
        rcp_menu = root.find(".//menuitem[@id='menu_scenarios_rcp']")
        if rcp_menu is None:
            print("❌ Menu scénarios RCP manquant")
            return False
        
        # Vérifier les sous-menus RCP
        generation_menu = root.find(".//menuitem[@id='menu_rcp_generation']")
        scenarios_menu = root.find(".//menuitem[@id='menu_rcp_scenarios']")
        donnees_menu = root.find(".//menuitem[@id='menu_rcp_donnees']")
        analyse_menu = root.find(".//menuitem[@id='menu_rcp_analyse']")
        
        # Debug: afficher ce qui est trouvé
        print(f"   - Menu génération: {'✅' if generation_menu is not None else '❌'}")
        print(f"   - Menu scénarios: {'✅' if scenarios_menu is not None else '❌'}")
        print(f"   - Menu données: {'✅' if donnees_menu is not None else '❌'}")
        print(f"   - Menu analyse: {'✅' if analyse_menu is not None else '❌'}")
        
        if generation_menu is not None and scenarios_menu is not None and donnees_menu is not None and analyse_menu is not None:
            print("✅ Structure du menu RCP correcte")
            return True
        else:
            print("❌ Sous-menus RCP manquants")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test du menu RCP: {e}")
        return False

def test_rcp_actions():
    """Test des actions RCP"""
    print("🔍 Test des actions RCP...")
    
    try:
        tree = ET.parse('smart_agri_decision/views/actions.xml')
        root = tree.getroot()
        
        # Vérifier l'action de génération automatique
        action_generation = root.find(".//record[@id='action_generer_scenarios_rcp']")
        if action_generation is None:
            print("❌ Action de génération RCP manquante")
            return False
        
        # Vérifier l'action des scénarios RCP
        action_scenarios = root.find(".//record[@id='action_rcp_scenarios']")
        if action_scenarios is None:
            print("❌ Action des scénarios RCP manquante")
            return False
        
        # Vérifier l'action des données annuelles
        action_donnees = root.find(".//record[@id='action_rcp_donnees_annuelles']")
        if action_donnees is None:
            print("❌ Action des données annuelles RCP manquante")
            return False
        
        print("✅ Actions RCP correctes")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des actions RCP: {e}")
        return False

def test_rcp_views():
    """Test des vues RCP"""
    print("🔍 Test des vues RCP...")
    
    try:
        tree = ET.parse('smart_agri_decision/views/rcp_views.xml')
        root = tree.getroot()
        
        # Vérifier la vue de génération
        vue_generation = root.find(".//record[@id='view_rcp_scenario_generation']")
        if vue_generation is None:
            print("❌ Vue de génération RCP manquante")
            return False
        
        # Vérifier la vue kanban
        vue_kanban = root.find(".//record[@id='view_rcp_scenario_kanban']")
        if vue_kanban is None:
            print("❌ Vue kanban RCP manquante")
            return False
        
        # Vérifier la vue formulaire
        vue_form = root.find(".//record[@id='view_rcp_scenario_form']")
        if vue_form is None:
            print("❌ Vue formulaire RCP manquante")
            return False
        
        print("✅ Vues RCP correctes")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des vues RCP: {e}")
        return False

def test_rcp_model():
    """Test du modèle RCP"""
    print("🔍 Test du modèle RCP...")
    
    try:
        with open('smart_agri_decision/models/rcp_scenario.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les méthodes de génération
        if 'generer_scenarios_rcp_standard' not in content:
            print("❌ Méthode de génération RCP manquante")
            return False
        
        if 'action_analyser_scenarios' not in content:
            print("❌ Méthode d'analyse RCP manquante")
            return False
        
        if 'action_exporter_analyse' not in content:
            print("❌ Méthode d'export RCP manquante")
            return False
        
        # Vérifier les scénarios RCP
        rcp_scenarios = ['RCP 2.6', 'RCP 4.5', 'RCP 6.0', 'RCP 8.5']
        for scenario in rcp_scenarios:
            if scenario not in content:
                print(f"❌ Scénario {scenario} manquant dans le modèle")
                return False
        
        print("✅ Modèle RCP correct")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du modèle RCP: {e}")
        return False

def test_rcp_demo_data():
    """Test des données de démonstration RCP"""
    print("🔍 Test des données de démonstration RCP...")
    
    try:
        tree = ET.parse('smart_agri_decision/data/demo_rcp_scenarios.xml')
        root = tree.getroot()
        
        # Vérifier les 4 scénarios RCP
        scenarios = root.findall(".//record[@model='rcp.scenario']")
        if len(scenarios) != 4:
            print(f"❌ Nombre de scénarios incorrect: {len(scenarios)} au lieu de 4")
            return False
        
        # Vérifier les données annuelles
        donnees_annuelles = root.findall(".//record[@model='rcp.donnee.annuelle']")
        if len(donnees_annuelles) < 12:  # Au moins 3 années par scénario
            print(f"❌ Nombre de données annuelles insuffisant: {len(donnees_annuelles)}")
            return False
        
        print("✅ Données de démonstration RCP correctes")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des données de démonstration RCP: {e}")
        return False

def test_manifest_integration():
    """Test de l'intégration dans le manifest"""
    print("🔍 Test de l'intégration dans le manifest...")
    
    try:
        with open('smart_agri_decision/__manifest__.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier l'inclusion des données RCP
        if 'demo_rcp_scenarios.xml' not in content:
            print("❌ Données RCP non incluses dans le manifest")
            return False
        
        print("✅ Intégration manifest RCP correcte")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du manifest RCP: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test des Scénarios RCP IPCC dans Smart Agri Decision")
    print("=" * 60)
    
    tests = [
        test_rcp_menu_structure,
        test_rcp_actions,
        test_rcp_views,
        test_rcp_model,
        test_rcp_demo_data,
        test_manifest_integration
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution du test: {e}")
            results.append(False)
    
    # Résumé des tests
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS RCP IPCC")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, result in enumerate(results):
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        test_name = tests[i].__name__.replace('_', ' ').title()
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 Résultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests RCP IPCC sont passés avec succès !")
        return 0
    else:
        print("⚠️ Certains tests RCP IPCC ont échoué. Vérifiez l'implémentation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
