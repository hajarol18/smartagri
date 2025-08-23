from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class MeteoData(models.Model):
    _name = 'meteo.data'
    _description = 'Données météorologiques'
    _order = 'date desc'

    # Informations de base
    name = fields.Char('Nom', required=True, default='Données météo')
    date = fields.Date('Date', required=True, default=fields.Date.today)
    heure = fields.Float('Heure (décimal)', help='Heure au format décimal (ex: 14.5 = 14h30)')
    
    # Coordonnées géographiques
    latitude = fields.Float('Latitude', digits=(16, 8), required=True)
    longitude = fields.Float('Longitude', digits=(16, 8), required=True)
    altitude = fields.Float('Altitude (m)', digits=(8, 2))
    
    # Données météorologiques
    temperature = fields.Float('Température (°C)', digits=(5, 2))
    temperature_min = fields.Float('Température min (°C)', digits=(5, 2))
    temperature_max = fields.Float('Température max (°C)', digits=(5, 2))
    
    humidite = fields.Float('Humidité relative (%)', digits=(5, 2))
    pression = fields.Float('Pression atmosphérique (hPa)', digits=(7, 2))
    
    precipitation = fields.Float('Précipitations (mm)', digits=(6, 2))
    precipitation_prob = fields.Float('Probabilité de pluie (%)', digits=(5, 2))
    
    vent_vitesse = fields.Float('Vitesse du vent (km/h)', digits=(5, 2))
    vent_direction = fields.Float('Direction du vent (°)', digits=(5, 2))
    
    rayonnement_solaire = fields.Float('Rayonnement solaire (W/m²)', digits=(6, 2))
    evapotranspiration = fields.Float('Évapotranspiration (mm)', digits=(5, 2))
    
    # Indices et alertes
    indice_uv = fields.Float('Indice UV', digits=(3, 1))
    indice_qualite_air = fields.Float('Indice qualité air', digits=(3, 1))
    
    # Alertes météorologiques
    alerte_secheresse = fields.Boolean('Alerte sécheresse')
    alerte_gel = fields.Boolean('Alerte gel')
    alerte_canicule = fields.Boolean('Alerte canicule')
    alerte_inondation = fields.Boolean('Alerte inondation')
    alerte_vent = fields.Boolean('Alerte vent fort')
    
    # Source des données
    source = fields.Selection([
        ('meteostat', 'Meteostat API'),
        ('meteo_france', 'Météo France'),
        ('station_locale', 'Station locale'),
        ('manuelle', 'Saisie manuelle')
    ], string='Source', default='meteostat', required=True)
    
    # Liens avec l'agriculture
    exploitation_id = fields.Many2one('exploitation.agri', string='Exploitation')
    parcelle_id = fields.Many2one('parcelle.agri', string='Parcelle')
    
    # Notes et observations
    notes = fields.Text('Notes')
    
    # Calculs automatiques
    stress_hydrique = fields.Float('Stress hydrique', compute='_compute_stress_hydrique', store=True)
    stress_thermique = fields.Float('Stress thermique', compute='_compute_stress_thermique', store=True)
    
    @api.depends('temperature', 'humidite', 'precipitation', 'evapotranspiration')
    def _compute_stress_hydrique(self):
        """Calcule le stress hydrique basé sur la disponibilité en eau"""
        for record in self:
            if record.evapotranspiration and record.precipitation:
                # Formule simplifiée : stress = (ET - P) / ET
                stress = (record.evapotranspiration - record.precipitation) / record.evapotranspiration
                record.stress_hydrique = max(0, min(1, stress))  # Entre 0 et 1
            else:
                record.stress_hydrique = 0.0
    
    @api.depends('temperature', 'temperature_min', 'temperature_max')
    def _compute_stress_thermique(self):
        """Calcule le stress thermique basé sur les températures"""
        for record in self:
            if record.temperature:
                # Stress thermique basé sur l'écart par rapport à l'optimum (20°C)
                optimum = 20.0
                ecart = abs(record.temperature - optimum)
                if ecart > 10:  # Stress significatif au-delà de 10°C d'écart
                    stress = min(1.0, ecart / 20.0)  # Normalisé entre 0 et 1
                else:
                    stress = 0.0
                record.stress_thermique = stress
            else:
                record.stress_thermique = 0.0
    
    @api.model
    def create(self, vals):
        """Surcharge de la création pour ajouter des validations"""
        # Validation des coordonnées
        if 'latitude' in vals and (vals['latitude'] < -90 or vals['latitude'] > 90):
            raise ValueError('Latitude doit être entre -90 et 90')
        if 'longitude' in vals and (vals['longitude'] < -180 or vals['longitude'] > 180):
            raise ValueError('Longitude doit être entre -180 et 180')
        
        # Validation des températures
        if 'temperature' in vals and vals['temperature'] < -100:
            raise ValueError('Température trop basse')
        if 'temperature' in vals and vals['temperature'] > 100:
            raise ValueError('Température trop élevée')
        
        return super().create(vals)
    
    def action_verifier_alertes(self):
        """Vérifie et met à jour les alertes météorologiques"""
        for record in self:
            # Alerte sécheresse
            if record.precipitation and record.precipitation < 1.0:  # Moins de 1mm
                record.alerte_secheresse = True
            else:
                record.alerte_secheresse = False
            
            # Alerte gel
            if record.temperature and record.temperature < 0:
                record.alerte_gel = True
            else:
                record.alerte_gel = False
            
            # Alerte canicule
            if record.temperature and record.temperature > 35:
                record.alerte_canicule = True
            else:
                record.alerte_canicule = False
            
            # Alerte inondation
            if record.precipitation and record.precipitation > 50:  # Plus de 50mm
                record.alerte_inondation = True
            else:
                record.alerte_inondation = False
            
            # Alerte vent fort
            if record.vent_vitesse and record.vent_vitesse > 50:  # Plus de 50 km/h
                record.alerte_vent = True
            else:
                record.alerte_vent = False
    
    def get_donnees_meteo(self, latitude, longitude, date_debut, date_fin):
        """Récupère les données météo pour une période donnée"""
        return self.search([
            ('latitude', '=', latitude),
            ('longitude', '=', longitude),
            ('date', '>=', date_debut),
            ('date', '<=', date_fin)
        ], order='date asc')
    
    def get_moyennes_periode(self, latitude, longitude, date_debut, date_fin):
        """Calcule les moyennes météorologiques sur une période"""
        donnees = self.get_donnees_meteo(latitude, longitude, date_debut, date_fin)
        
        if not donnees:
            return {}
        
        moyennes = {
            'temperature': sum(d.temperature or 0 for d in donnees) / len(donnees),
            'humidite': sum(d.humidite or 0 for d in donnees) / len(donnees),
            'precipitation': sum(d.precipitation or 0 for d in donnees),
            'vent_vitesse': sum(d.vent_vitesse or 0 for d in donnees) / len(donnees),
            'rayonnement_solaire': sum(d.rayonnement_solaire or 0 for d in donnees) / len(donnees),
        }
        
        return moyennes
