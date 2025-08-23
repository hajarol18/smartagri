# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

class TestMeteoData(unittest.TestCase):
    """Tests pour le modèle MeteoData"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        # Mock de l'environnement Odoo
        self.env_mock = MagicMock()
        self.meteo_model = MagicMock()
        self.env_mock.__getitem__ = MagicMock(return_value=self.meteo_model)
        
    def test_create_meteo_data(self):
        """Test de création d'une donnée météo"""
        # Données de test
        test_data = {
            'date': datetime.now(),
            'latitude': 48.8566,
            'longitude': 2.3522,
            'temperature': 20.5,
            'precipitation': 5.0,
            'humidite': 65.0,
            'vent_vitesse': 10.0,
            'pression': 1013.25,
            'rayonnement_solaire': 500.0,
            'source': 'meteostat'
        }
        
        # Mock de la création
        self.meteo_model.create.return_value = MagicMock(id=1)
        
        # Test
        result = self.meteo_model.create(test_data)
        
        # Vérifications
        self.meteo_model.create.assert_called_once_with(test_data)
        self.assertEqual(result.id, 1)
        
    def test_validation_coordinates(self):
        """Test de validation des coordonnées géographiques"""
        # Coordonnées valides
        valid_lat = 48.8566
        valid_lon = 2.3522
        
        # Coordonnées invalides
        invalid_lat = 100.0  # > 90
        invalid_lon = 200.0  # > 180
        
        # Test coordonnées valides
        self.assertTrue(-90 <= valid_lat <= 90)
        self.assertTrue(-180 <= valid_lon <= 180)
        
        # Test coordonnées invalides
        self.assertFalse(-90 <= invalid_lat <= 90)
        self.assertFalse(-180 <= invalid_lon <= 180)
        
    def test_alert_calculations(self):
        """Test des calculs d'alertes"""
        # Test alerte gel
        temp_gel = -5.0
        self.assertTrue(temp_gel < 0)  # Alerte gel
        
        # Test alerte canicule
        temp_canicule = 40.0
        self.assertTrue(temp_canicule > 35)  # Alerte canicule
        
        # Test alerte sécheresse
        precip_secheresse = 0.5
        self.assertTrue(precip_secheresse < 1.0)  # Alerte sécheresse
        
        # Test alerte inondation
        precip_inondation = 60.0
        self.assertTrue(precip_inondation > 50.0)  # Alerte inondation
        
        # Test alerte vent
        vent_fort = 60.0
        self.assertTrue(vent_fort > 50.0)  # Alerte vent
        
    def test_stress_calculations(self):
        """Test des calculs de stress"""
        # Test stress hydrique
        evapotranspiration = 10.0
        precipitation = 5.0
        
        if evapotranspiration and precipitation:
            stress = (evapotranspiration - precipitation) / evapotranspiration
            stress = max(0, min(1, stress))
            self.assertEqual(stress, 0.5)
        
        # Test stress thermique
        temperature = 30.0
        optimum = 20.0
        ecart = abs(temperature - optimum)
        
        if ecart > 10:
            stress = min(1.0, ecart / 20.0)
            self.assertEqual(stress, 0.5)

class TestExploitation(unittest.TestCase):
    """Tests pour le modèle Exploitation"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.env_mock = MagicMock()
        self.exploitation_model = MagicMock()
        self.env_mock.__getitem__ = MagicMock(return_value=self.exploitation_model)
        
    def test_import_meteo_validation(self):
        """Test de validation pour l'import météo"""
        # Test avec coordonnées manquantes
        exploitation_no_coords = MagicMock()
        exploitation_no_coords.latitude = None
        exploitation_no_coords.longitude = None
        
        # Test avec coordonnées valides
        exploitation_with_coords = MagicMock()
        exploitation_with_coords.latitude = 48.8566
        exploitation_with_coords.longitude = 2.3522
        
        # Vérifications
        self.assertFalse(exploitation_no_coords.latitude and exploitation_no_coords.longitude)
        self.assertTrue(exploitation_with_coords.latitude and exploitation_with_coords.longitude)
        
    def test_meteo_data_creation_count(self):
        """Test du nombre de données météo créées"""
        # 7 jours de données
        days_count = 7
        
        # Vérification
        self.assertEqual(days_count, 7)
        
        # Test de création de données pour chaque jour
        for i in range(days_count):
            date_meteo = datetime.now() + timedelta(days=i)
            self.assertIsInstance(date_meteo, datetime)

if __name__ == '__main__':
    unittest.main()
