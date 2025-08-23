from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Culture(models.Model):
    _name = 'culture.agri'
    _description = 'Culture Agricole'
    _rec_name = 'nom'

    nom = fields.Char(string="Nom de la culture", required=True)
    nom_scientifique = fields.Char(string="Nom scientifique")
    famille = fields.Selection([
        ('cereales', 'Céréales'),
        ('legumineuses', 'Légumineuses'),
        ('oleagineux', 'Oléo-protéagineux'),
        ('legumes', 'Légumes'),
        ('fruits', 'Fruits'),
        ('vigne', 'Vigne'),
        ('autres', 'Autres'),
    ], string="Famille de culture")
    
    # Cycle cultural
    duree_cycle = fields.Integer(string="Durée du cycle (jours)")
    saison_plantation = fields.Selection([
        ('printemps', 'Printemps'),
        ('ete', 'Été'),
        ('automne', 'Automne'),
        ('hiver', 'Hiver'),
        ('toute_annee', 'Toute l\'année'),
    ], string="Saison de plantation")
    
    # Rendements
    rendement_moyen = fields.Float(string="Rendement moyen (t/ha)")
    rendement_min = fields.Float(string="Rendement minimum (t/ha)")
    rendement_max = fields.Float(string="Rendement maximum (t/ha)")
    
    # Besoins climatiques
    temperature_min = fields.Float(string="Température minimum (°C)")
    temperature_opt = fields.Float(string="Température optimale (°C)")
    temperature_max = fields.Float(string="Température maximum (°C)")
    besoin_eau = fields.Selection([
        ('faible', 'Faible'),
        ('moyen', 'Moyen'),
        ('eleve', 'Élevé'),
    ], string="Besoin en eau")
    
    # Besoins pédologiques
    type_sol_prefere = fields.Selection([
        ('argileux', 'Argileux'),
        ('limoneux', 'Limoneux'),
        ('sableux', 'Sableux'),
        ('calcaire', 'Calcaire'),
        ('humifere', 'Humifère'),
    ], string="Type de sol préféré")
    
    ph_min = fields.Float(string="pH minimum")
    ph_max = fields.Float(string="pH maximum")
    
    # Résistance aux stress
    resistance_secheresse = fields.Selection([
        ('faible', 'Faible'),
        ('moyenne', 'Moyenne'),
        ('elevee', 'Élevée'),
    ], string="Résistance à la sécheresse")
    
    resistance_gel = fields.Selection([
        ('faible', 'Faible'),
        ('moyenne', 'Moyenne'),
        ('elevee', 'Élevée'),
    ], string="Résistance au gel")
    
    # Relations
    exploitation_id = fields.Many2one('exploitation.agri', string="Exploitation")
    parcelle_id = fields.Many2one('parcelle.agri', string="Parcelle")
    
    # Historique
    date_semis = fields.Date(string="Date de semis")
    date_recolte = fields.Date(string="Date de récolte")
    rendement_effectif = fields.Float(string="Rendement effectif (t/ha)")
    etat_culture = fields.Selection([
        ('planifiee', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('abandonnee', 'Abandonnée'),
    ], string="État de la culture", default='planifiee')
    
    # Notes
    notes = fields.Text(string="Notes")
    
    @api.constrains('rendement_moyen', 'rendement_min', 'rendement_max')
    def _check_rendements(self):
        for record in self:
            if record.rendement_min > record.rendement_max:
                raise ValidationError("Le rendement minimum ne peut pas être supérieur au rendement maximum.")
            if record.rendement_moyen < record.rendement_min or record.rendement_moyen > record.rendement_max:
                raise ValidationError("Le rendement moyen doit être entre le minimum et le maximum.")
    
    @api.constrains('temperature_min', 'temperature_opt', 'temperature_max')
    def _check_temperatures(self):
        for record in self:
            if record.temperature_min > record.temperature_max:
                raise ValidationError("La température minimum ne peut pas être supérieure à la température maximum.")
            if record.temperature_opt < record.temperature_min or record.temperature_opt > record.temperature_max:
                raise ValidationError("La température optimale doit être entre le minimum et le maximum.") 