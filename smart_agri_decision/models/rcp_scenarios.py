from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class RcpScenario(models.Model):
    _name = 'rcp.scenario'
    _description = 'Scénarios RCP IPCC'
    _order = 'annee, scenario'

    # Informations de base
    name = fields.Char('Nom', required=True, default='Scénario RCP')
    scenario = fields.Selection([
        ('rcp26', 'RCP 2.6 - Faible émission'),
        ('rcp45', 'RCP 4.5 - Émission modérée'),
        ('rcp60', 'RCP 6.0 - Émission élevée'),
        ('rcp85', 'RCP 8.5 - Émission très élevée')
    ], string='Scénario RCP', required=True, default='rcp45')
    
    annee = fields.Integer('Année de projection', required=True, default=2050)
    description = fields.Text('Description du scénario')
    
    # Coordonnées géographiques
    latitude = fields.Float('Latitude', digits=(16, 8), required=True)
    longitude = fields.Float('Longitude', digits=(16, 8), required=True)
    
    # Projections climatiques
    temperature_moyenne = fields.Float('Température moyenne (°C)', digits=(5, 2))
    temperature_min = fields.Float('Température min (°C)', digits=(5, 2))
    temperature_max = fields.Float('Température max (°C)', digits=(5, 2))
    
    precipitation_annuelle = fields.Float('Précipitations annuelles (mm)', digits=(8, 2))
    secheresse_frequence = fields.Float('Fréquence des sécheresses (%)', digits=(5, 2))
    canicule_frequence = fields.Float('Fréquence des canicules (%)', digits=(5, 2))
    
    # Impacts agricoles
    rendement_blé = fields.Float('Impact sur rendement blé (%)', digits=(5, 2))
    rendement_mais = fields.Float('Impact sur rendement maïs (%)', digits=(5, 2))
    rendement_riz = fields.Float('Impact sur rendement riz (%)', digits=(5, 2))
    
    stress_hydrique = fields.Float('Stress hydrique projeté', digits=(5, 2))
    stress_thermique = fields.Float('Stress thermique projeté', digits=(5, 2))
    
    # Adaptation et mitigation
    adaptation_irrigation = fields.Boolean('Adaptation irrigation nécessaire')
    adaptation_varietes = fields.Boolean('Adaptation variétés nécessaires')
    adaptation_dates = fields.Boolean('Adaptation dates semis nécessaires')
    
    cout_adaptation = fields.Float('Coût adaptation (€/ha)', digits=(10, 2))
    benefice_adaptation = fields.Float('Bénéfice adaptation (€/ha)', digits=(10, 2))
    
    # Source et fiabilité
    source_donnees = fields.Selection([
        ('ipcc_ar6', 'IPCC AR6'),
        ('meteostat', 'Meteostat projections'),
        ('cnrm', 'CNRM-CM6'),
        ('ipsl', 'IPSL-CM6A-LR'),
        ('autre', 'Autre source')
    ], string='Source des données', default='ipcc_ar6')
    
    niveau_confiance = fields.Selection([
        ('faible', 'Faible'),
        ('moyen', 'Moyen'),
        ('eleve', 'Élevé'),
        ('tres_eleve', 'Très élevé')
    ], string='Niveau de confiance', default='moyen')
    
    # Liens avec l'agriculture
    exploitation_id = fields.Many2one('exploitation.agri', string='Exploitation')
    parcelle_id = fields.Many2one('parcelle.agri', string='Parcelle')
    
    # Calculs automatiques
    impact_global = fields.Float('Impact global (%)', compute='_compute_impact_global', store=True)
    rentabilite_adaptation = fields.Float('Rentabilité adaptation', compute='_compute_rentabilite_adaptation', store=True)
    
    @api.depends('rendement_blé', 'rendement_mais', 'rendement_riz')
    def _compute_impact_global(self):
        """Calcule l'impact global sur les rendements"""
        for record in self:
            impacts = []
            if record.rendement_blé:
                impacts.append(abs(record.rendement_blé))
            if record.rendement_mais:
                impacts.append(abs(record.rendement_mais))
            if record.rendement_riz:
                impacts.append(abs(record.rendement_riz))
            
            if impacts:
                record.impact_global = sum(impacts) / len(impacts)
            else:
                record.impact_global = 0.0
    
    @api.depends('cout_adaptation', 'benefice_adaptation')
    def _compute_rentabilite_adaptation(self):
        """Calcule la rentabilité des mesures d'adaptation"""
        for record in self:
            if record.cout_adaptation and record.benefice_adaptation:
                record.rentabilite_adaptation = record.benefice_adaptation - record.cout_adaptation
            else:
                record.rentabilite_adaptation = 0.0
    
    @api.model
    def get_scenarios_par_zone(self, latitude, longitude, annee=2050):
        """Récupère tous les scénarios RCP pour une zone géographique"""
        return self.search([
            ('latitude', '=', latitude),
            ('longitude', '=', longitude),
            ('annee', '=', annee)
        ], order='scenario')
    
    @api.model
    def get_comparaison_scenarios(self, latitude, longitude, annee=2050):
        """Compare les différents scénarios RCP pour une zone"""
        scenarios = self.get_scenarios_par_zone(latitude, longitude, annee)
        
        comparaison = {}
        for scenario in scenarios:
            comparaison[scenario.scenario] = {
                'temperature': scenario.temperature_moyenne,
                'precipitation': scenario.precipitation_annuelle,
                'impact_blé': scenario.rendement_blé,
                'impact_mais': scenario.rendement_mais,
                'stress_hydrique': scenario.stress_hydrique,
                'cout_adaptation': scenario.cout_adaptation
            }
        
        return comparaison
    
    def action_simuler_impact(self):
        """Simule l'impact du scénario sur l'agriculture"""
        for record in self:
            # Simulation basée sur les projections
            if record.temperature_moyenne:
                # Impact sur les cultures selon la température
                if record.temperature_moyenne > 25:
                    record.stress_thermique = 0.8
                    record.adaptation_varietes = True
                elif record.temperature_moyenne > 20:
                    record.stress_thermique = 0.4
                    record.adaptation_varietes = False
                else:
                    record.stress_thermique = 0.0
                    record.adaptation_varietes = False
            
            if record.precipitation_annuelle:
                # Impact sur l'irrigation
                if record.precipitation_annuelle < 600:  # Moins de 600mm/an
                    record.stress_hydrique = 0.9
                    record.adaptation_irrigation = True
                elif record.precipitation_annuelle < 800:
                    record.stress_hydrique = 0.6
                    record.adaptation_irrigation = True
                else:
                    record.stress_hydrique = 0.2
                    record.adaptation_irrigation = False
    
    def get_recommandations_adaptation(self):
        """Génère des recommandations d'adaptation basées sur le scénario"""
        recommandations = []
        
        for record in self:
            if record.adaptation_irrigation:
                recommandations.append("Système d'irrigation goutte-à-goutte recommandé")
            
            if record.adaptation_varietes:
                recommandations.append("Sélection de variétés résistantes à la chaleur")
            
            if record.adaptation_dates:
                recommandations.append("Ajustement des dates de semis et récolte")
            
            if record.stress_hydrique > 0.7:
                recommandations.append("Mise en place de techniques de conservation de l'eau")
            
            if record.stress_thermique > 0.7:
                recommandations.append("Installation d'ombrières ou brise-vent")
        
        return recommandations
    
    @api.model
    def create(self, vals):
        """Surcharge de la création pour ajouter des validations"""
        # Validation des coordonnées
        if 'latitude' in vals and (vals['latitude'] < -90 or vals['latitude'] > 90):
            raise ValueError('Latitude doit être entre -90 et 90')
        if 'longitude' in vals and (vals['longitude'] < -180 or vals['longitude'] > 180):
            raise ValueError('Longitude doit être entre -180 et 180')
        
        # Validation de l'année
        if 'annee' in vals and (vals['annee'] < 2020 or vals['annee'] > 2100):
            raise ValueError('Année doit être entre 2020 et 2100')
        
        return super().create(vals)
