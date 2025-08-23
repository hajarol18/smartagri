from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Intrant(models.Model):
    _name = 'intrant.agri'
    _description = 'Intrant Agricole'
    _rec_name = 'nom'

    nom = fields.Char(string="Nom de l'intrant", required=True)
    
    # Type d'intrant
    type_intrant = fields.Selection([
        ('semences', 'Semences'),
        ('engrais', 'Engrais'),
        ('pesticides', 'Pesticides'),
        ('eau', 'Eau'),
        ('carburant', 'Carburant'),
        ('main_oeuvre', 'Main d\'œuvre'),
        ('materiel', 'Matériel'),
        ('autre', 'Autre'),
    ], string="Type d'intrant", required=True)
    
    # Catégorie détaillée
    categorie = fields.Selection([
        # Semences
        ('cereales', 'Céréales'),
        ('legumineuses', 'Légumineuses'),
        ('oleagineux', 'Oléo-protéagineux'),
        ('legumes', 'Légumes'),
        ('fruits', 'Fruits'),
        # Engrais
        ('azote', 'Azote (N)'),
        ('phosphore', 'Phosphore (P)'),
        ('potassium', 'Potassium (K)'),
        ('organique', 'Organique'),
        ('complexe', 'Complexe NPK'),
        # Pesticides
        ('herbicide', 'Herbicide'),
        ('fongicide', 'Fongicide'),
        ('insecticide', 'Insecticide'),
        ('acaricide', 'Acaricide'),
        # Eau
        ('irrigation', 'Irrigation'),
        ('pluie', 'Eau de pluie'),
        # Autres
        ('carburant_diesel', 'Diesel'),
        ('carburant_essence', 'Essence'),
        ('main_oeuvre_saisonniere', 'Main d\'œuvre saisonnière'),
        ('main_oeuvre_permanente', 'Main d\'œuvre permanente'),
        ('materiel_location', 'Location matériel'),
        ('materiel_achat', 'Achat matériel'),
    ], string="Catégorie")
    
    # Caractéristiques
    unite = fields.Selection([
        ('kg', 'Kilogrammes'),
        ('l', 'Litres'),
        ('m3', 'Mètres cubes'),
        ('ha', 'Hectares'),
        ('h', 'Heures'),
        ('jour', 'Jours'),
        ('unite', 'Unités'),
    ], string="Unité de mesure", required=True)
    
    quantite = fields.Float(string="Quantité", required=True)
    prix_unitaire = fields.Float(string="Prix unitaire (€)")
    cout_total = fields.Float(string="Coût total (€)", compute='_compute_cout_total', store=True)
    
    # Qualité et spécifications
    qualite = fields.Selection([
        ('excellente', 'Excellente'),
        ('bonne', 'Bonne'),
        ('moyenne', 'Moyenne'),
        ('mauvaise', 'Mauvaise'),
    ], string="Qualité")
    
    specifications = fields.Text(string="Spécifications techniques")
    
    # Relations
    exploitation_id = fields.Many2one('exploitation.agri', string="Exploitation")
    parcelle_id = fields.Many2one('parcelle.agri', string="Parcelle")
    intervention_id = fields.Many2one('intervention.agri', string="Intervention")
    culture_id = fields.Many2one('culture.agri', string="Culture")
    
    # Dates
    date_achat = fields.Date(string="Date d'achat")
    date_utilisation = fields.Date(string="Date d'utilisation")
    date_peremption = fields.Date(string="Date de péremption")
    
    # Stock
    stock_disponible = fields.Float(string="Stock disponible")
    stock_minimum = fields.Float(string="Stock minimum")
    localisation_stock = fields.Char(string="Localisation du stock")
    
    # Fournisseur
    fournisseur = fields.Char(string="Fournisseur")
    numero_lot = fields.Char(string="Numéro de lot")
    
    # Impact environnemental
    impact_environnemental = fields.Selection([
        ('faible', 'Faible'),
        ('moyen', 'Moyen'),
        ('eleve', 'Élevé'),
    ], string="Impact environnemental")
    
    # Notes
    notes = fields.Text(string="Notes")
    
    @api.depends('quantite', 'prix_unitaire')
    def _compute_cout_total(self):
        for record in self:
            record.cout_total = record.quantite * record.prix_unitaire
    
    @api.constrains('quantite', 'prix_unitaire')
    def _check_valeurs_positives(self):
        for record in self:
            if record.quantite < 0:
                raise ValidationError("La quantité ne peut pas être négative.")
            if record.prix_unitaire < 0:
                raise ValidationError("Le prix unitaire ne peut pas être négatif.")
    
    @api.onchange('type_intrant')
    def _onchange_type_intrant(self):
        if self.type_intrant:
            # Définir des valeurs par défaut selon le type d'intrant
            if self.type_intrant == 'semences':
                self.unite = 'kg'
                self.categorie = 'cereales'
            elif self.type_intrant == 'engrais':
                self.unite = 'kg'
                self.categorie = 'azote'
            elif self.type_intrant == 'eau':
                self.unite = 'm3'
                self.categorie = 'irrigation'
            elif self.type_intrant == 'carburant':
                self.unite = 'l'
                self.categorie = 'carburant_diesel'
            elif self.type_intrant == 'main_oeuvre':
                self.unite = 'h'
                self.categorie = 'main_oeuvre_saisonniere'
    
    def action_utiliser(self):
        """Marquer l'intrant comme utilisé"""
        for record in self:
            if record.stock_disponible >= record.quantite:
                record.stock_disponible -= record.quantite
                record.date_utilisation = fields.Date.today()
            else:
                raise ValidationError("Stock insuffisant pour cette utilisation.")
    
    @api.model
    def get_stock_alert(self):
        """Retourner les intrants avec stock faible"""
        return self.search([
            ('stock_disponible', '<=', 'stock_minimum'),
            ('stock_disponible', '>', 0)
        ]) 