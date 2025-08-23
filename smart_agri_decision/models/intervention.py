from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Intervention(models.Model):
    _name = 'intervention.agri'
    _description = 'Intervention Agricole'
    _rec_name = 'nom'
    _order = 'date_intervention desc'

    nom = fields.Char(string="Nom de l'intervention", required=True)
    
    # Type d'intervention
    type_intervention = fields.Selection([
        ('preparation_sol', 'Préparation du sol'),
        ('semis', 'Semis'),
        ('plantation', 'Plantation'),
        ('irrigation', 'Irrigation'),
        ('fertilisation', 'Fertilisation'),
        ('traitement_phyto', 'Traitement phytosanitaire'),
        ('desherbage', 'Désherbage'),
        ('recolte', 'Récolte'),
        ('taille', 'Taille'),
        ('autre', 'Autre'),
    ], string="Type d'intervention", required=True)
    
    # Planification
    date_planifiee = fields.Date(string="Date planifiée")
    date_intervention = fields.Date(string="Date d'intervention")
    duree_estimee = fields.Float(string="Durée estimée (heures)")
    duree_effective = fields.Float(string="Durée effective (heures)")
    
    # État
    etat = fields.Selection([
        ('planifiee', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ], string="État", default='planifiee')
    
    # Localisation
    exploitation_id = fields.Many2one('exploitation.agri', string="Exploitation", required=True)
    parcelle_id = fields.Many2one('parcelle.agri', string="Parcelle")
    culture_id = fields.Many2one('culture.agri', string="Culture concernée")
    
    # Détails techniques
    description = fields.Text(string="Description détaillée")
    observations = fields.Text(string="Observations")
    
    # Intrants utilisés
    intrants_ids = fields.One2many('intrant.agri', 'intervention_id', string="Intrants utilisés")
    
    # Coûts
    cout_estime = fields.Float(string="Coût estimé (€)")
    cout_effectif = fields.Float(string="Coût effectif (€)")
    
    # Conditions météo
    temperature = fields.Float(string="Température (°C)")
    humidite = fields.Float(string="Humidité (%)")
    vitesse_vent = fields.Float(string="Vitesse du vent (km/h)")
    conditions_meteo = fields.Selection([
        ('ensoleille', 'Ensoleillé'),
        ('nuageux', 'Nuageux'),
        ('pluvieux', 'Pluvieux'),
        ('venteux', 'Venteux'),
        ('orageux', 'Orageux'),
    ], string="Conditions météo")
    
    # Ressources humaines
    nombre_personnes = fields.Integer(string="Nombre de personnes")
    cout_main_oeuvre = fields.Float(string="Coût main d'œuvre (€)")
    
    # Équipements
    equipements_utilises = fields.Text(string="Équipements utilisés")
    
    # Priorité
    priorite = fields.Selection([
        ('basse', 'Basse'),
        ('normale', 'Normale'),
        ('haute', 'Haute'),
        ('urgente', 'Urgente'),
    ], string="Priorité", default='normale')
    
    # Validation
    validee_par = fields.Many2one('res.users', string="Validée par")
    date_validation = fields.Datetime(string="Date de validation")
    
    @api.constrains('date_planifiee', 'date_intervention')
    def _check_dates(self):
        for record in self:
            if record.date_intervention and record.date_planifiee:
                if record.date_intervention < record.date_planifiee:
                    raise ValidationError("La date d'intervention ne peut pas être antérieure à la date planifiée.")
    
    @api.constrains('duree_estimee', 'duree_effective')
    def _check_durees(self):
        for record in self:
            if record.duree_estimee and record.duree_estimee < 0:
                raise ValidationError("La durée estimée ne peut pas être négative.")
            if record.duree_effective and record.duree_effective < 0:
                raise ValidationError("La durée effective ne peut pas être négative.")
    
    @api.onchange('type_intervention')
    def _onchange_type_intervention(self):
        if self.type_intervention:
            # Définir des valeurs par défaut selon le type d'intervention
            if self.type_intervention == 'irrigation':
                self.duree_estimee = 2.0
            elif self.type_intervention == 'fertilisation':
                self.duree_estimee = 1.5
            elif self.type_intervention == 'recolte':
                self.duree_estimee = 4.0
            else:
                self.duree_estimee = 1.0
    
    def action_terminer(self):
        """Marquer l'intervention comme terminée"""
        for record in self:
            record.etat = 'terminee'
            record.date_intervention = fields.Date.today()
    
    def action_annuler(self):
        """Annuler l'intervention"""
        for record in self:
            record.etat = 'annulee' 