from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import json

class RCPScenario(models.Model):
    _name = 'rcp.scenario'
    _description = 'Scénario RCP IPCC'
    _rec_name = 'name'
    _order = 'name'

    # Champs de base
    name = fields.Char(string="Nom du scénario", required=True)
    description = fields.Text(string="Description")
    rcp_type = fields.Selection([
        ('rcp_26', 'RCP 2.6 (Optimiste)'),
        ('rcp_45', 'RCP 4.5 (Intermédiaire)'),
        ('rcp_60', 'RCP 6.0 (Intermédiaire-élevé)'),
        ('rcp_85', 'RCP 8.5 (Pessimiste)')
    ], string="Type RCP", required=True, default='rcp_45')
    
    # Relations (optionnelles pour les scénarios RCP)
    exploitation_id = fields.Many2one('exploitation.agri', string="Exploitation de référence", required=False, help="Exploitation optionnelle pour l'analyse locale")
    parcelle_id = fields.Many2one('parcelle.agri', string="Parcelle de référence", help="Parcelle optionnelle pour l'analyse locale")
    
    # Période d'étude
    annee_debut = fields.Integer(string="Année de début", required=True, default=2020)
    annee_fin = fields.Integer(string="Année de fin", required=True, default=2100)
    duree_etude = fields.Integer(string="Durée d'étude (années)", compute='_compute_duree_etude', store=True)
    
    # État
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('active', 'Actif'),
        ('archived', 'Archivé')
    ], string="État", default='draft', required=True)
    
    # Paramètres climatiques - Températures
    temperature_rise = fields.Float(string="Élévation de température (°C)", digits=(4, 2))
    temperature_min_change = fields.Float(string="Changement température min (°C)", digits=(4, 2))
    temperature_max_change = fields.Float(string="Changement température max (°C)", digits=(4, 2))
    temperature_optimum = fields.Float(string="Température optimale (°C)", digits=(4, 2))
    
    # Paramètres climatiques - Gaz à effet de serre
    co2_concentration = fields.Float(string="Concentration CO2 (ppm)", digits=(6, 2))
    ch4_concentration = fields.Float(string="Concentration CH4 (ppb)", digits=(6, 2))
    n2o_concentration = fields.Float(string="Concentration N2O (ppb)", digits=(6, 2))
    forcage_radiatif = fields.Float(string="Forçage radiatif (W/m²)", digits=(4, 2))
    
    # Paramètres climatiques - Précipitations
    precipitation_change = fields.Float(string="Changement précipitations (%)", digits=(5, 2))
    intensite_pluie_change = fields.Float(string="Changement intensité pluie (%)", digits=(5, 2))
    frequence_secheresse = fields.Float(string="Fréquence sécheresse (jours/an)", digits=(5, 2))
    
    # Paramètres climatiques - Autres
    humidite_change = fields.Float(string="Changement humidité (%)", digits=(5, 2))
    vent_change = fields.Float(string="Changement vent (%)", digits=(5, 2))
    ensoleillement_change = fields.Float(string="Changement ensoleillement (%)", digits=(5, 2))
    
    # Impacts agricoles - Stress hydrique
    stress_hydrique_rcp = fields.Float(string="Stress hydrique RCP (0-1)", digits=(3, 2))
    evapotranspiration_change = fields.Float(string="Changement évapotranspiration (%)", digits=(5, 2))
    reserve_eau_change = fields.Float(string="Changement réserve eau (%)", digits=(5, 2))
    
    # Impacts agricoles - Stress thermique
    stress_thermique_rcp = fields.Float(string="Stress thermique RCP (0-1)", digits=(3, 2))
    degres_jour_change = fields.Float(string="Changement degrés-jour (%)", digits=(5, 2))
    periode_vegetation_change = fields.Float(string="Changement période végétation (jours)", digits=(5, 2))
    
    # Impacts agricoles - Rendements
    rendement_change = fields.Float(string="Changement rendement (%)", digits=(5, 2))
    qualite_produit_change = fields.Float(string="Changement qualité produit (%)", digits=(5, 2))
    risque_perte = fields.Float(string="Risque de perte (%)", digits=(5, 2))
    
    # Impacts agricoles - Adaptation
    strategies_adaptation = fields.Text(string="Stratégies d'adaptation")
    cout_adaptation = fields.Float(string="Coût adaptation (€/ha)", digits=(10, 2))
    efficacite_adaptation = fields.Float(string="Efficacité adaptation (%)", digits=(5, 2))
    
    # Données temporelles
    donnees_annuelles_ids = fields.One2many('rcp.donnee.annuelle', 'scenario_id', string="Données annuelles")
    
    # Graphiques et analyses
    graphique_temperature = fields.Binary(string="Graphique température")
    graphique_precipitation = fields.Binary(string="Graphique précipitations")
    graphique_stress = fields.Binary(string="Graphique stress")
    graphique_rendement = fields.Binary(string="Graphique rendement")
    
    # Métadonnées
    create_date = fields.Datetime(string="Date de création", readonly=True)
    write_date = fields.Datetime(string="Dernière modification", readonly=True)
    create_uid = fields.Many2one('res.users', string="Créé par", readonly=True)
    write_uid = fields.Many2one('res.users', string="Modifié par", readonly=True)
    
    @api.depends('annee_debut', 'annee_fin')
    def _compute_duree_etude(self):
        for record in self:
            if record.annee_debut and record.annee_fin:
                record.duree_etude = record.annee_fin - record.annee_debut + 1
            else:
                record.duree_etude = 0
    
    @api.constrains('annee_debut', 'annee_fin')
    def _check_annees(self):
        for record in self:
            if record.annee_debut and record.annee_fin:
                if record.annee_debut > record.annee_fin:
                    raise ValidationError("L'année de début doit être antérieure à l'année de fin.")
                if record.annee_debut < 2020 or record.annee_fin > 2100:
                    raise ValidationError("Les années doivent être comprises entre 2020 et 2100.")
    
    @api.onchange('rcp_type')
    def _onchange_rcp_type(self):
        """Définit automatiquement les paramètres selon le type RCP"""
        if self.rcp_type:
            rcp_params = self._get_rcp_parameters()
            self.temperature_rise = rcp_params.get('temperature_rise', 0)
            self.co2_concentration = rcp_params.get('co2_concentration', 0)
            self.precipitation_change = rcp_params.get('precipitation_change', 0)
            self.stress_hydrique_rcp = rcp_params.get('stress_hydrique_rcp', 0)
            self.stress_thermique_rcp = rcp_params.get('stress_thermique_rcp', 0)
            self.rendement_change = rcp_params.get('rendement_change', 0)
    
    def _get_rcp_parameters(self):
        """Retourne les paramètres par défaut selon le type RCP"""
        params = {
            'rcp_26': {
                'temperature_rise': 1.0,
                'co2_concentration': 421,
                'precipitation_change': -5,
                'stress_hydrique_rcp': 0.1,
                'stress_thermique_rcp': 0.05,
                'rendement_change': -2.5
            },
            'rcp_45': {
                'temperature_rise': 1.8,
                'co2_concentration': 538,
                'precipitation_change': -8,
                'stress_hydrique_rcp': 0.15,
                'stress_thermique_rcp': 0.12,
                'rendement_change': -5.0
            },
            'rcp_60': {
                'temperature_rise': 2.2,
                'co2_concentration': 670,
                'precipitation_change': -12,
                'stress_hydrique_rcp': 0.25,
                'stress_thermique_rcp': 0.20,
                'rendement_change': -8.5
            },
            'rcp_85': {
                'temperature_rise': 3.7,
                'co2_concentration': 936,
                'precipitation_change': -20,
                'stress_hydrique_rcp': 0.40,
                'stress_thermique_rcp': 0.35,
                'rendement_change': -15.0
            }
        }
        return params.get(self.rcp_type, {})
    
    def action_activer(self):
        """Active le scénario RCP"""
        self.ensure_one()
        if self.state == 'draft':
            self.state = 'active'
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Scénario Activé',
                    'message': f'Le scénario {self.name} est maintenant actif.',
                    'type': 'success',
                }
            }
    
    def action_archiver(self):
        """Archive le scénario RCP"""
        self.ensure_one()
        if self.state == 'active':
            self.state = 'archived'
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Scénario Archivé',
                    'message': f'Le scénario {self.name} a été archivé.',
                    'type': 'warning',
                }
            }
    
    def action_dupliquer(self):
        """Duplique le scénario RCP"""
        self.ensure_one()
        new_scenario = self.copy({
            'name': f"{self.name} (Copie)",
            'state': 'draft',
            'annee_debut': 2020,
            'annee_fin': 2100
        })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'rcp.scenario',
            'res_id': new_scenario.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def generer_donnees_annuelles(self):
        """Génère automatiquement les données annuelles pour le scénario"""
        self.ensure_one()
        
        # Supprimer les anciennes données
        self.donnees_annuelles_ids.unlink()
        
        donnees = []
        for annee in range(self.annee_debut, self.annee_fin + 1):
            # Calculer les valeurs selon l'année et le type RCP
            facteur_temps = (annee - self.annee_debut) / (self.annee_fin - self.annee_debut)
            
            donnee = {
                'scenario_id': self.id,
                'annee': annee,
                'temperature_moyenne': 15 + (self.temperature_rise * facteur_temps),
                'precipitation_totale': 800 * (1 + self.precipitation_change / 100 * facteur_temps),
                'stress_hydrique': min(1.0, self.stress_hydrique_rcp * facteur_temps),
                'stress_thermique': min(1.0, self.stress_thermique_rcp * facteur_temps),
                'rendement_projete': 100 * (1 + self.rendement_change / 100 * facteur_temps)
            }
            donnees.append(donnee)
        
        # Créer les enregistrements
        self.env['rcp.donnee.annuelle'].create(donnees)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Données Générées',
                'message': f'{len(donnees)} années de données ont été générées pour le scénario {self.name}.',
                'type': 'success',
            }
        }
    
    def calculer_impacts(self):
        """Calcule les impacts du scénario sur l'agriculture"""
        self.ensure_one()
        
        # Calculs simplifiés des impacts
        if self.temperature_rise > 2.0:
            self.stress_thermique_rcp = min(1.0, (self.temperature_rise - 2.0) / 3.0)
        else:
            self.stress_thermique_rcp = 0.0
        
        if self.precipitation_change < -10:
            self.stress_hydrique_rcp = min(1.0, abs(self.precipitation_change) / 50)
        else:
            self.stress_hydrique_rcp = 0.0
        
        # Impact sur les rendements
        impact_temp = -self.stress_thermique_rcp * 15  # -15% max pour stress thermique
        impact_hydrique = -self.stress_hydrique_rcp * 20  # -20% max pour stress hydrique
        self.rendement_change = impact_temp + impact_hydrique
        
        return True

    def generer_scenarios_rcp_standard(self):
        """Génère automatiquement les 4 scénarios RCP IPCC standard"""
        # Vérifier s'il existe déjà des scénarios
        scenarios_existants = self.search([])
        if scenarios_existants:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Scénarios déjà existants',
                    'message': f'{len(scenarios_existants)} scénarios RCP sont déjà disponibles.',
                    'type': 'info',
                }
            }
        
        # Créer les scénarios RCP standard
        rcp_scenarios = [
            {
                'name': 'RCP 2.6 - Optimiste',
                'description': 'Scénario de stabilisation avec émissions très faibles. Stabilisation de la température à +1°C d\'ici 2100.',
                'rcp_type': 'rcp_26',
                'annee_debut': 2020,
                'annee_fin': 2100,
                'temperature_rise': 1.0,
                'co2_concentration': 421,
                'precipitation_change': -5,
                'stress_hydrique_rcp': 0.1,
                'stress_thermique_rcp': 0.05,
                'rendement_change': -2.5
            },
            {
                'name': 'RCP 4.5 - Intermédiaire',
                'description': 'Scénario de stabilisation modérée. Stabilisation de la température à +1.8°C d\'ici 2100.',
                'rcp_type': 'rcp_45',
                'annee_debut': 2020,
                'annee_fin': 2100,
                'temperature_rise': 1.8,
                'co2_concentration': 538,
                'precipitation_change': -8,
                'stress_hydrique_rcp': 0.15,
                'stress_thermique_rcp': 0.12,
                'rendement_change': -5.0
            },
            {
                'name': 'RCP 6.0 - Élevé',
                'description': 'Scénario avec émissions élevées. Augmentation de la température à +2.2°C d\'ici 2100.',
                'rcp_type': 'rcp_60',
                'annee_debut': 2020,
                'annee_fin': 2100,
                'temperature_rise': 2.2,
                'co2_concentration': 670,
                'precipitation_change': -12,
                'stress_hydrique_rcp': 0.25,
                'stress_thermique_rcp': 0.20,
                'rendement_change': -8.5
            },
            {
                'name': 'RCP 8.5 - Pessimiste',
                'description': 'Scénario avec émissions très élevées. Augmentation de la température à +3.7°C d\'ici 2100.',
                'rcp_type': 'rcp_85',
                'annee_debut': 2020,
                'annee_fin': 2100,
                'temperature_rise': 3.7,
                'co2_concentration': 936,
                'precipitation_change': -20,
                'stress_hydrique_rcp': 0.40,
                'stress_thermique_rcp': 0.35,
                'rendement_change': -15.0
            }
        ]
        
        # Créer les scénarios
        scenarios_crees = []
        for rcp_data in rcp_scenarios:
            # Les scénarios RCP sont des projections climatiques GLOBALES
            # Pas besoin de les lier à une exploitation spécifique
            scenario = self.create(rcp_data)
            scenarios_crees.append(scenario)
            
            # Générer les données annuelles pour ce scénario
            scenario.generer_donnees_annuelles()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Scénarios RCP générés !',
                'message': f'4 scénarios RCP IPCC ont été créés avec leurs données annuelles jusqu\'en 2100.',
                'type': 'success',
            }
        }

    def action_analyser_scenarios(self):
        """Analyse et compare les scénarios RCP actifs"""
        self.ensure_one()
        scenarios_actifs = self.search([('state', '=', 'active')])
        
        if not scenarios_actifs:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Aucun scénario actif',
                    'message': 'Aucun scénario RCP n\'est actuellement actif.',
                    'type': 'warning',
                }
            }
        
        # Calculer les statistiques comparatives
        analyses = []
        for scenario in scenarios_actifs:
            analyse = {
                'scenario': scenario.name,
                'type_rcp': scenario.rcp_type,
                'temperature_rise': scenario.temperature_rise,
                'impact_rendement': scenario.rendement_change,
                'stress_hydrique': scenario.stress_hydrique_rcp,
                'stress_thermique': scenario.stress_thermique_rcp
            }
            analyses.append(analyse)
        
        # Afficher l'analyse
        message = "Analyse comparative des scénarios RCP actifs:\n\n"
        for analyse in analyses:
            message += f"• {analyse['scenario']} ({analyse['type_rcp']}):\n"
            message += f"  - Élévation température: +{analyse['temperature_rise']}°C\n"
            message += f"  - Impact rendement: {analyse['impact_rendement']}%\n"
            message += f"  - Stress hydrique: {analyse['stress_hydrique']:.2f}\n"
            message += f"  - Stress thermique: {analyse['stress_thermique']:.2f}\n\n"
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Analyse des Scénarios RCP',
                'message': message,
                'type': 'info',
                'sticky': True,
            }
        }

    def action_exporter_analyse(self):
        """Exporte l'analyse des scénarios RCP en PDF"""
        self.ensure_one()
        # Ici on pourrait implémenter la génération de PDF
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Export PDF',
                'message': 'Fonctionnalité d\'export PDF en cours de développement.',
                'type': 'info',
            }
        }

    def action_generer_rapport_complet(self):
        """Génère un rapport PDF complet d'analyse des scénarios RCP"""
        self.ensure_one()
        # Ici on pourrait implémenter la génération de rapport PDF complet
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Rapport Complet',
                'message': 'Fonctionnalité de rapport PDF complet en cours de développement.',
                'type': 'info',
            }
        }


class RCPDonneeAnnuelle(models.Model):
    _name = 'rcp.donnee.annuelle'
    _description = 'Données annuelles RCP'
    _order = 'annee'
    
    scenario_id = fields.Many2one('rcp.scenario', string="Scénario RCP", required=True, ondelete='cascade')
    annee = fields.Integer(string="Année", required=True)
    temperature_moyenne = fields.Float(string="Température moyenne (°C)", digits=(4, 2))
    precipitation_totale = fields.Float(string="Précipitations totales (mm)", digits=(6, 2))
    stress_hydrique = fields.Float(string="Stress hydrique (0-1)", digits=(3, 2))
    stress_thermique = fields.Float(string="Stress thermique (0-1)", digits=(3, 2))
    rendement_projete = fields.Float(string="Rendement projeté (%)", digits=(5, 2))
    
    _sql_constraints = [
        ('unique_annee_scenario', 'unique(scenario_id, annee)', 'Une année ne peut être définie qu\'une fois par scénario.')
    ]
