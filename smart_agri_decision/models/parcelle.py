from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Parcelle(models.Model):
    _name = 'parcelle.agri'
    _description = 'Parcelle Agricole'
    _rec_name = 'nom'

    nom = fields.Char(string="Nom de la parcelle", required=True)
    code_parcelle = fields.Char(string="Code parcelle")
    
    # Géométrie (PostGIS)
    # geom = fields.GeoField(string="Géométrie", srid=4326)  # Pour PostGIS
    
    # Superficie
    superficie = fields.Float(string="Superficie (ha)", required=True)
    largeur = fields.Float(string="Largeur (m)")
    longueur = fields.Float(string="Longueur (m)")
    
    # Localisation
    exploitation_id = fields.Many2one('exploitation.agri', string="Exploitation", required=True)
    latitude = fields.Float(string="Latitude")
    longitude = fields.Float(string="Longitude")
    altitude = fields.Float(string="Altitude (m)")
    
    # Caractéristiques pédologiques
    type_sol = fields.Selection([
        ('argileux', 'Argileux'),
        ('limoneux', 'Limoneux'),
        ('sableux', 'Sableux'),
        ('calcaire', 'Calcaire'),
        ('humifere', 'Humifère'),
    ], string="Type de sol")
    
    ph_sol = fields.Float(string="pH du sol")
    taux_matiere_organique = fields.Float(string="Taux matière organique (%)")
    capacite_retention = fields.Float(string="Capacité de rétention (mm)")
    
    # Système d'irrigation
    systeme_irrigation = fields.Selection([
        ('aucun', 'Aucun'),
        ('aspersion', 'Aspersion'),
        ('goutte_goutte', 'Goutte à goutte'),
        ('gravitaire', 'Gravitaire'),
        ('pivot', 'Pivot'),
    ], string="Système d'irrigation", default='aucun')
    
    # État de la parcelle
    etat_parcelle = fields.Selection([
        ('en_culture', 'En culture'),
        ('en_jachere', 'En jachère'),
        ('en_preparation', 'En préparation'),
        ('abandonnee', 'Abandonnée'),
    ], string="État de la parcelle", default='en_preparation')
    
    # Cultures actuelles et historiques
    culture_actuelle_id = fields.Many2one('culture.agri', string="Culture actuelle")
    cultures_ids = fields.One2many('culture.agri', 'parcelle_id', string="Historique des cultures")
    
    # Interventions
    interventions_ids = fields.One2many('intervention.agri', 'parcelle_id', string="Interventions")
    
    # Rendements
    rendement_moyen = fields.Float(string="Rendement moyen (t/ha)", compute='_compute_rendement_moyen')
    
    # Notes
    notes = fields.Text(string="Notes")
    
    @api.depends('cultures_ids.rendement_effectif')
    def _compute_rendement_moyen(self):
        for record in self:
            cultures_terminees = record.cultures_ids.filtered(lambda c: c.etat_culture == 'terminee' and c.rendement_effectif > 0)
            if cultures_terminees:
                record.rendement_moyen = sum(cultures_terminees.mapped('rendement_effectif')) / len(cultures_terminees)
            else:
                record.rendement_moyen = 0.0
    
    @api.constrains('superficie')
    def _check_superficie(self):
        for record in self:
            if record.superficie <= 0:
                raise ValidationError("La superficie doit être positive.")
    
    @api.constrains('ph_sol')
    def _check_ph(self):
        for record in self:
            if record.ph_sol and (record.ph_sol < 0 or record.ph_sol > 14):
                raise ValidationError("Le pH doit être entre 0 et 14.") 