from odoo import models, fields, api
from datetime import datetime, timedelta

class MeteoData(models.Model):
    _name = "meteo.data"
    _description = "Données météorologiques"
    _order = "date desc"

    name = fields.Char(string="Nom", compute="_compute_name", store=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    exploitation_id = fields.Many2one("exploitation.agri", string="Exploitation")
    parcelle_id = fields.Many2one("parcelle.agri", string="Parcelle")
    
    # Données météorologiques
    temperature = fields.Float(string="Température (°C)")
    precipitation = fields.Float(string="Précipitations (mm)")
    humidite = fields.Float(string="Humidité relative (%)")
    rayonnement_solaire = fields.Float(string="Rayonnement solaire (W/m²)")
    vitesse_vent = fields.Float(string="Vitesse du vent (km/h)")
    
    # Alertes
    alerte_gel = fields.Boolean(string="Alerte Gel", default=False)
    alerte_canicule = fields.Boolean(string="Alerte Canicule", default=False)
    alerte_secheresse = fields.Boolean(string="Alerte Sécheresse", default=False)
    alerte_inondation = fields.Boolean(string="Alerte Inondation", default=False)
    alerte_vent = fields.Boolean(string="Alerte Vent", default=False)
    
    # Calculs automatiques
    stress_thermique = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé'),
        ('critique', 'Critique')
    ], string="Stress thermique", compute="_compute_stress_thermique", store=True)
    
    stress_hydrique = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé'),
        ('critique', 'Critique')
    ], string="Stress hydrique", compute="_compute_stress_hydrique", store=True)
    
    @api.depends('date', 'exploitation_id', 'parcelle_id')
    def _compute_name(self):
        for record in self:
            if record.date and record.exploitation_id:
                record.name = f"Météo {record.exploitation_id.name} - {record.date}"
            elif record.date:
                record.name = f"Météo - {record.date}"
            else:
                record.name = "Nouvelle donnée météo"
    
    @api.depends('temperature')
    def _compute_stress_thermique(self):
        for record in self:
            if not record.temperature:
                record.stress_thermique = 'faible'
            elif record.temperature < 0:
                record.stress_thermique = 'critique'
            elif record.temperature < 5:
                record.stress_thermique = 'eleve'
            elif record.temperature < 10:
                record.stress_thermique = 'modere'
            elif record.temperature > 35:
                record.stress_thermique = 'critique'
            elif record.temperature > 30:
                record.stress_thermique = 'eleve'
            elif record.temperature > 25:
                record.stress_thermique = 'modere'
            else:
                record.stress_thermique = 'faible'
    
    @api.depends('precipitation', 'humidite')
    def _compute_stress_hydrique(self):
        for record in self:
            if not record.precipitation and not record.humidite:
                record.stress_hydrique = 'faible'
            elif record.precipitation < 1 and record.humidite < 30:
                record.stress_hydrique = 'critique'
            elif record.precipitation < 5 and record.humidite < 50:
                record.stress_hydrique = 'eleve'
            elif record.precipitation < 10 and record.humidite < 60:
                record.stress_hydrique = 'modere'
            elif record.precipitation > 50:
                record.stress_hydrique = 'eleve'
            else:
                record.stress_hydrique = 'faible'
    
    @api.model
    def calculer_alertes_automatiques(self):
        """Calcule automatiquement les alertes météo"""
        records = self.search([])
        for record in records:
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
            
            # Alerte sécheresse
            if record.precipitation and record.precipitation < 1 and record.humidite and record.humidite < 30:
                record.alerte_secheresse = True
            else:
                record.alerte_secheresse = False
            
            # Alerte inondation
            if record.precipitation and record.precipitation > 50:
                record.alerte_inondation = True
            else:
                record.alerte_inondation = False
            
            # Alerte vent
            if record.vitesse_vent and record.vitesse_vent > 50:
                record.alerte_vent = True
            else:
                record.alerte_vent = False
