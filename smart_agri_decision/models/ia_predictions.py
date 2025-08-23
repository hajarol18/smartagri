from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class IaPrediction(models.Model):
    _name = 'ia.prediction'
    _description = 'Prédictions et recommandations IA'
    _order = 'date_creation desc'

    # Informations de base
    name = fields.Char('Nom', required=True, default='Prédiction IA')
    type_prediction = fields.Selection([
        ('rendement', 'Prédiction de rendement'),
        ('stress', 'Détection de stress'),
        ('recommandation', 'Recommandation culture'),
        ('optimisation', 'Optimisation ressources'),
        ('simulation', 'Simulation scénario')
    ], string='Type de prédiction', required=True, default='rendement')
    
    date_creation = fields.Datetime('Date de création', default=fields.Datetime.now)
    date_prediction = fields.Date('Date de prédiction', required=True)
    
    # Données d'entrée
    exploitation_id = fields.Many2one('exploitation.agri', string='Exploitation', required=True)
    parcelle_id = fields.Many2one('parcelle.agri', string='Parcelle')
    culture_id = fields.Many2one('culture.agri', string='Culture')
    
    # Coordonnées géographiques
    latitude = fields.Float('Latitude', digits=(16, 8), required=True)
    longitude = fields.Float('Longitude', digits=(16, 8), required=True)
    
    # Données météorologiques utilisées
    temperature_moyenne = fields.Float('Température moyenne (°C)', digits=(5, 2))
    precipitation_totale = fields.Float('Précipitations totales (mm)', digits=(6, 2))
    humidite_moyenne = fields.Float('Humidité moyenne (%)', digits=(5, 2))
    rayonnement_solaire = fields.Float('Rayonnement solaire (W/m²)', digits=(6, 2))
    
    # Données du sol
    ph_sol = fields.Float('pH du sol', digits=(3, 2))
    azote_sol = fields.Float('Azote du sol (mg/kg)', digits=(6, 2))
    phosphore_sol = fields.Float('Phosphore du sol (mg/kg)', digits=(6, 2))
    potassium_sol = fields.Float('Potassium du sol (mg/kg)', digits=(6, 2))
    
    # Prédictions IA
    rendement_predit = fields.Float('Rendement prédit (t/ha)', digits=(6, 2))
    rendement_confiance = fields.Float('Niveau de confiance (%)', digits=(5, 2))
    
    stress_hydrique_predit = fields.Float('Stress hydrique prédit', digits=(5, 2))
    stress_thermique_predit = fields.Float('Stress thermique prédit', digits=(5, 2))
    stress_nutritionnel_predit = fields.Float('Stress nutritionnel prédit', digits=(5, 2))
    
    # Recommandations
    recommandation_irrigation = fields.Text('Recommandation irrigation')
    recommandation_fertilisation = fields.Text('Recommandation fertilisation')
    recommandation_traitement = fields.Text('Recommandation traitement')
    recommandation_variete = fields.Text('Recommandation variété')
    
    # Optimisation des ressources
    eau_optimale = fields.Float('Eau optimale (L/m²)', digits=(6, 2))
    engrais_azote_opt = fields.Float('Engrais azote optimal (kg/ha)', digits=(6, 2))
    engrais_phosphore_opt = fields.Float('Engrais phosphore optimal (kg/ha)', digits=(6, 2))
    engrais_potassium_opt = fields.Float('Engrais potassium optimal (kg/ha)', digits=(6, 2))
    
    # Coûts et bénéfices
    cout_optimisation = fields.Float('Coût optimisation (€/ha)', digits=(10, 2))
    benefice_attendu = fields.Float('Bénéfice attendu (€/ha)', digits=(10, 2))
    rentabilite = fields.Float('Rentabilité (€/ha)', compute='_compute_rentabilite', store=True)
    
    # Modèle IA utilisé
    modele_ia = fields.Selection([
        ('regression_lineaire', 'Régression linéaire'),
        ('random_forest', 'Random Forest'),
        ('xgboost', 'XGBoost'),
        ('reseau_neurones', 'Réseau de neurones'),
        ('svm', 'Support Vector Machine')
    ], string='Modèle IA utilisé', default='random_forest')
    
    version_modele = fields.Char('Version du modèle')
    precision_modele = fields.Float('Précision du modèle (%)', digits=(5, 2))
    
    # Statut et validation
    statut = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('valide', 'Validé'),
        ('applique', 'Appliqué'),
        ('archive', 'Archivé')
    ], string='Statut', default='brouillon')
    
    notes = fields.Text('Notes et observations')
    
    @api.depends('cout_optimisation', 'benefice_attendu')
    def _compute_rentabilite(self):
        """Calcule la rentabilité de l'optimisation"""
        for record in self:
            if record.cout_optimisation and record.benefice_attendu:
                record.rentabilite = record.benefice_attendu - record.cout_optimisation
            else:
                record.rentabilite = 0.0
    
    @api.model
    def predire_rendement(self, exploitation_id, parcelle_id, culture_id, date_prediction):
        """Prédit le rendement pour une culture donnée"""
        # Simulation d'une prédiction IA
        prediction = self.create({
            'name': f'Prédiction rendement {culture_id.name}',
            'type_prediction': 'rendement',
            'date_prediction': date_prediction,
            'exploitation_id': exploitation_id,
            'parcelle_id': parcelle_id,
            'culture_id': culture_id,
            'rendement_predit': 8.5,  # Simulation
            'rendement_confiance': 85.0,
            'statut': 'valide'
        })
        
        return prediction
    
    @api.model
    def detecter_stress(self, exploitation_id, parcelle_id):
        """Détecte les stress sur une parcelle"""
        # Simulation de détection de stress
        stress = self.create({
            'name': f'Détection stress {parcelle_id.name}',
            'type_prediction': 'stress',
            'date_prediction': fields.Date.today(),
            'exploitation_id': exploitation_id,
            'parcelle_id': parcelle_id,
            'stress_hydrique_predit': 0.7,
            'stress_thermique_predit': 0.3,
            'statut': 'valide'
        })
        
        return stress
    
    @api.model
    def generer_recommandations(self, exploitation_id, parcelle_id, culture_id):
        """Génère des recommandations pour une culture"""
        # Simulation de recommandations
        recommandation = self.create({
            'name': f'Recommandations {culture_id.name}',
            'type_prediction': 'recommandation',
            'date_prediction': fields.Date.today(),
            'exploitation_id': exploitation_id,
            'parcelle_id': parcelle_id,
            'culture_id': culture_id,
            'recommandation_irrigation': 'Irrigation goutte-à-goutte recommandée',
            'recommandation_fertilisation': 'Apport azote modéré nécessaire',
            'statut': 'valide'
        })
        
        return recommandation
    
    @api.model
    def optimiser_ressources(self, exploitation_id, parcelle_id):
        """Optimise l'utilisation des ressources"""
        # Simulation d'optimisation
        optimisation = self.create({
            'name': f'Optimisation ressources {parcelle_id.name}',
            'type_prediction': 'optimisation',
            'date_prediction': fields.Date.today(),
            'exploitation_id': exploitation_id,
            'parcelle_id': parcelle_id,
            'eau_optimale': 25.0,
            'engrais_azote_opt': 120.0,
            'cout_optimisation': 150.0,
            'benefice_attendu': 300.0,
            'statut': 'valide'
        })
        
        return optimisation
    
    def action_appliquer_recommandations(self):
        """Applique les recommandations de l'IA"""
        for record in self:
            if record.statut == 'valide':
                record.statut = 'applique'
                
                # Créer une intervention basée sur les recommandations
                if record.recommandation_irrigation:
                    self.env['intervention.agri'].create({
                        'name': f'Intervention IA: {record.recommandation_irrigation}',
                        'type_intervention': 'irrigation',
                        'date_intervention': fields.Date.today(),
                        'exploitation_id': record.exploitation_id.id,
                        'parcelle_id': record.parcelle_id.id,
                        'notes': f'Recommandation IA: {record.recommandation_irrigation}'
                    })
                
                if record.recommandation_fertilisation:
                    self.env['intervention.agri'].create({
                        'name': f'Intervention IA: {record.recommandation_fertilisation}',
                        'type_intervention': 'fertilisation',
                        'date_intervention': fields.Date.today(),
                        'exploitation_id': record.exploitation_id.id,
                        'parcelle_id': record.parcelle_id.id,
                        'notes': f'Recommandation IA: {record.recommandation_fertilisation}'
                    })
    
    def get_historique_predictions(self, exploitation_id, parcelle_id, type_prediction=None):
        """Récupère l'historique des prédictions"""
        domain = [
            ('exploitation_id', '=', exploitation_id),
            ('parcelle_id', '=', parcelle_id)
        ]
        
        if type_prediction:
            domain.append(('type_prediction', '=', type_prediction))
        
        return self.search(domain, order='date_creation desc')
    
    def get_precision_globale(self):
        """Calcule la précision globale des prédictions"""
        predictions_validees = self.search([('statut', '=', 'applique')])
        
        if not predictions_validees:
            return 0.0
        
        precision_totale = sum(p.rendement_confiance or 0 for p in predictions_validees)
        return precision_totale / len(predictions_validees)
    
    @api.model
    def create(self, vals):
        """Surcharge de la création pour ajouter des validations"""
        # Validation des coordonnées
        if 'latitude' in vals and (vals['latitude'] < -90 or vals['latitude'] > 90):
            raise ValueError('Latitude doit être entre -90 et 90')
        if 'longitude' in vals and (vals['longitude'] < -180 or vals['longitude'] > 180):
            raise ValueError('Longitude doit être entre -180 et 180')
        
        # Validation des pourcentages
        if 'rendement_confiance' in vals and (vals['rendement_confiance'] < 0 or vals['rendement_confiance'] > 100):
            raise ValueError('Niveau de confiance doit être entre 0 et 100')
        
        return super().create(vals)
