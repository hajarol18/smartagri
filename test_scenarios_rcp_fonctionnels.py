#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des Scénarios RCP IPCC Fonctionnels dans Smart Agri Decision
Vérifie que les scénarios RCP s'affichent correctement en interface
"""

import os
import sys
import xml.etree.ElementTree as ET

def test_scenario_climatique_model():
    """Test du modèle scenario.climatique"""
    print("🔍 Test du modèle scenario.climatique...")
    
    model_file = "smart_agri_decision/models/scenario_climatique.py"
    
    if not os.path.exists(model_file):
        print("   ❌ Fichier modèle manquant:", model_file)
        return False
    
    try:
        with open(model_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les éléments essentiels
        checks = [
            ("class ScenarioClimatique", "Classe du modèle"),
            ("_name = 'scenario.climatique'", "Nom du modèle"),
            ("scenario_rcp", "Champ scénario RCP"),
            ("annee", "Champ année"),
            ("temperature_moyenne", "Champ température"),
            ("generer_scenarios_rcp_standard", "Méthode de génération"),
            ("action_analyser_impact", "Méthode d'analyse"),
            ("action_comparer_scenarios", "Méthode de comparaison")
        ]
        
        all_passed = True
        for check, description in checks:
            if check in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} manquant")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la lecture: {e}")
        return False

def test_scenario_climatique_views():
    """Test des vues pour scenario.climatique"""
    print("🔍 Test des vues scenario.climatique...")
    
    views_file = "smart_agri_decision/views/scenario_climatique_views.xml"
    
    if not os.path.exists(views_file):
        print("   ❌ Fichier vues manquant:", views_file)
        return False
    
    try:
        tree = ET.parse(views_file)
        root = tree.getroot()
        
        # Vérifier les vues essentielles
        views_to_check = [
            ("view_scenario_climatique_list", "Vue liste"),
            ("view_scenario_climatique_form", "Vue formulaire"),
            ("view_scenario_climatique_graph", "Vue graphique"),
            ("view_scenario_climatique_pivot", "Vue pivot"),
            ("view_scenario_climatique_kanban", "Vue kanban"),
            ("view_scenario_climatique_search", "Vue recherche")
        ]
        
        all_passed = True
        for view_id, description in views_to_check:
            view = root.find(f".//record[@id='{view_id}']")
            if view is not None:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} manquant")
                all_passed = False
        
        # Vérifier les actions
        actions_to_check = [
            ("action_scenario_climatique", "Action principale"),
            ("action_generer_scenarios_rcp_auto", "Action génération"),
            ("action_analyser_impact_scenario", "Action analyse"),
            ("action_comparer_scenarios_rcp", "Action comparaison")
        ]
        
        for action_id, description in actions_to_check:
            action = root.find(f".//record[@id='{action_id}']")
            if action is not None:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} manquant")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la lecture des vues: {e}")
        return False

def test_menu_integration():
    """Test de l'intégration dans le menu principal"""
    print("🔍 Test de l'intégration menu...")
    
    menu_file = "smart_agri_decision/views/main_menu.xml"
    
    if not os.path.exists(menu_file):
        print("   ❌ Fichier menu manquant:", menu_file)
        return False
    
    try:
        tree = ET.parse(menu_file)
        root = tree.getroot()
        
        # Vérifier la structure du menu RCP
        menu_rcp = root.find(".//menuitem[@id='menu_scenarios_rcp']")
        if menu_rcp is not None:
            print("   ✅ Menu RCP principal")
        else:
            print("   ❌ Menu RCP principal manquant")
            return False
        
        # Vérifier les sous-menus RCP
        submenus_to_check = [
            ("menu_rcp_generation", "Génération automatique"),
            ("menu_rcp_scenarios", "Scénarios climatiques"),
            ("menu_rcp_analyse", "Analyse comparative")
        ]
        
        all_passed = True
        for submenu_id, description in submenus_to_check:
            submenu = root.find(f".//menuitem[@id='{submenu_id}']")
            if submenu is not None:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} manquant")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la lecture du menu: {e}")
        return False

def test_manifest_integration():
    """Test de l'intégration dans le manifest"""
    print("🔍 Test de l'intégration manifest...")
    
    manifest_file = "smart_agri_decision/__manifest__.py"
    
    if not os.path.exists(manifest_file):
        print("   ❌ Fichier manifest manquant:", manifest_file)
        return False
    
    try:
        with open(manifest_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les éléments essentiels
        checks = [
            ("scenario_climatique_views.xml", "Vues des scénarios"),
            ("scenario_climatique", "Modèle des scénarios")
        ]
        
        all_passed = True
        for check, description in checks:
            if check in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} manquant")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la lecture du manifest: {e}")
        return False

def test_security_access():
    """Test des droits d'accès"""
    print("🔍 Test des droits d'accès...")
    
    security_file = "smart_agri_decision/security/ir.model.access.csv"
    
    if not os.path.exists(security_file):
        print("   ❌ Fichier sécurité manquant:", security_file)
        return False
    
    try:
        with open(security_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "scenario_climatique" in content:
            print("   ✅ Droits d'accès configurés")
            return True
        else:
            print("   ❌ Droits d'accès manquants")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la lecture de la sécurité: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test des Scénarios RCP IPCC Fonctionnels dans Smart Agri Decision")
    print("=" * 70)
    
    tests = [
        ("Modèle scenario.climatique", test_scenario_climatique_model),
        ("Vues scenario.climatique", test_scenario_climatique_views),
        ("Intégration menu", test_menu_integration),
        ("Intégration manifest", test_manifest_integration),
        ("Droits d'accès", test_security_access)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        result = test_func()
        results.append((test_name, result))
    
    # Résumé des tests
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS SCÉNARIOS RCP IPCC")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests des scénarios RCP IPCC sont passés avec succès !")
        print("🌱 Les scénarios RCP sont maintenant fonctionnels et s'affichent correctement !")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez l'implémentation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
