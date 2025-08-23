from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import json

class Parcelle(models.Model):
    _name = 'parcelle.agri'
    _description = 'Parcelle Agricole'
    _rec_name = 'nom'
    _order = 'nom'

    # Informations de base
    nom = fields.Char(string="Nom de la parcelle", required=True)
    code_parcelle = fields.Char(string="Code parcelle")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('active', 'Active'),
        ('archived', 'Archivée')
    ], string="État", default='draft', required=True)
    
    # Géométrie et surface
    surface = fields.Float(string="Surface déclarée", digits=(8, 2))
    surface_calculee = fields.Float(string="Surface calculée (ha)", digits=(8, 4), readonly=True)
    unite_surface = fields.Selection([
        ('ha', 'Hectares'),
        ('m2', 'Mètres carrés'),
        ('acres', 'Acres')
    ], string="Unité de surface", default='ha', required=True)
    
    # Géolocalisation
    exploitation_id = fields.Many2one('exploitation.agri', string="Exploitation", required=True, ondelete='cascade')
    latitude = fields.Float(string="Latitude", digits=(10, 6))
    longitude = fields.Float(string="Longitude", digits=(10, 6))
    altitude = fields.Float(string="Altitude (m)", digits=(6, 2))
    coordonnees_gps = fields.Text(string="Coordonnées GPS", readonly=True)
    
    # Carte Leaflet
    carte_parcelle = fields.Text(string="Carte Parcelle", help="Données de la carte Leaflet")
    geometrie_parcelle = fields.Text(string="Géométrie Parcelle", help="Coordonnées du polygone de la parcelle")
    
    # Culture
    culture_id = fields.Many2one('culture.agri', string="Culture actuelle")
    date_plantation = fields.Date(string="Date de plantation")
    date_recolte_prevue = fields.Date(string="Date de récolte prévue")
    
    # Caractéristiques du sol
    type_sol = fields.Selection([
        ('argileux', 'Argileux'),
        ('limoneux', 'Limoneux'),
        ('sableux', 'Sableux'),
        ('calcaire', 'Calcaire'),
        ('humifere', 'Humifère'),
        ('loameux', 'Loameux'),
        ('tourbeux', 'Tourbeux'),
    ], string="Type de sol")
    
    ph_sol = fields.Float(string="pH du sol", digits=(3, 1))
    materiau_organique = fields.Float(string="Matière organique (%)", digits=(4, 2))
    capacite_retention_eau = fields.Float(string="Capacité de rétention d'eau (mm)", digits=(6, 2))
    
    # Irrigation et drainage
    systeme_irrigation = fields.Selection([
        ('aucun', 'Aucun'),
        ('aspersion', 'Aspersion'),
        ('goutte_goutte', 'Goutte à goutte'),
        ('gravitaire', 'Gravitaire'),
        ('pivot', 'Pivot'),
        ('rampe', 'Rampe mobile'),
        ('micro_aspersion', 'Micro-aspersion'),
    ], string="Système d'irrigation", default='aucun')
    
    besoin_eau = fields.Float(string="Besoin en eau (mm/jour)", digits=(5, 2))
    efficacite_irrigation = fields.Float(string="Efficacité irrigation (%)", digits=(5, 2))
    systeme_drainage = fields.Selection([
        ('aucun', 'Aucun'),
        ('naturel', 'Naturel'),
        ('tuyaux', 'Tuyaux drainants'),
        ('fosses', 'Fosses de drainage'),
        ('drains', 'Drains enterrés'),
    ], string="Système de drainage", default='aucun')
    
    # Gestion des cultures
    rotation_culture = fields.Selection([
        ('annuelle', 'Annuelle'),
        ('bienale', 'Bienale'),
        ('triennale', 'Triennale'),
        ('quadriennale', 'Quadriennale'),
        ('permanente', 'Permanente'),
    ], string="Rotation des cultures", default='annuelle')
    
    densite_plantation = fields.Float(string="Densité de plantation (plantes/m²)", digits=(6, 2))
    espacement_rangs = fields.Float(string="Espacement entre rangs (cm)", digits=(5, 2))
    espacement_plantes = fields.Float(string="Espacement entre plantes (cm)", digits=(5, 2))
    
    # Suivi et maintenance
    derniere_intervention = fields.Date(string="Dernière intervention")
    prochaine_intervention = fields.Date(string="Prochaine intervention prévue")
    notes = fields.Text(string="Notes et observations")
    
    # Relations
    intervention_ids = fields.One2many('intervention.agri', 'parcelle_id', string="Interventions")
    meteo_data_ids = fields.One2many('meteo.data', 'parcelle_id', string="Données météo")
    historique_ids = fields.One2many('parcelle.historique', 'parcelle_id', string="Historique")
    
    # Champs calculés
    rendement_moyen = fields.Float(string="Rendement moyen (t/ha)", digits=(6, 2), compute='_compute_rendement_moyen', store=True)
    age_culture = fields.Integer(string="Âge de la culture (jours)", compute='_compute_age_culture')
    stress_hydrique = fields.Float(string="Stress hydrique (0-1)", digits=(3, 2), compute='_compute_stress_hydrique')
    stress_thermique = fields.Float(string="Stress thermique (0-1)", digits=(3, 2), compute='_compute_stress_thermique')
    
    # Contraintes
    _sql_constraints = [
        ('unique_code_parcelle', 'unique(code_parcelle)', 'Le code parcelle doit être unique.'),
        ('check_surface_positive', 'CHECK(surface >= 0)', 'La surface doit être positive.'),
        ('check_ph_range', 'CHECK(ph_sol >= 0 AND ph_sol <= 14)', 'Le pH doit être entre 0 et 14.'),
    ]

    @api.depends('intervention_ids.rendement_effectif')
    def _compute_rendement_moyen(self):
        for record in self:
            interventions_terminees = record.intervention_ids.filtered(
                lambda i: i.type_intervention == 'recolte' and i.rendement_effectif > 0
            )
            if interventions_terminees:
                record.rendement_moyen = sum(interventions_terminees.mapped('rendement_effectif')) / len(interventions_terminees)
            else:
                record.rendement_moyen = 0.0

    @api.depends('date_plantation')
    def _compute_age_culture(self):
        for record in self:
            if record.date_plantation:
                delta = datetime.now().date() - record.date_plantation
                record.age_culture = delta.days
            else:
                record.age_culture = 0

    @api.depends('meteo_data_ids.stress_hydrique')
    def _compute_stress_hydrique(self):
        for record in self:
            if record.meteo_data_ids:
                # Prendre la moyenne des 7 derniers jours
                recent_data = record.meteo_data_ids.sorted('date', reverse=True)[:7]
                if recent_data:
                    record.stress_hydrique = sum(recent_data.mapped('stress_hydrique')) / len(recent_data)
                else:
                    record.stress_hydrique = 0.0
            else:
                record.stress_hydrique = 0.0

    @api.depends('meteo_data_ids.stress_thermique')
    def _compute_stress_thermique(self):
        for record in self:
            if record.meteo_data_ids:
                # Prendre la moyenne des 7 derniers jours
                recent_data = record.meteo_data_ids.sorted('date', reverse=True)[:7]
                if recent_data:
                    record.stress_thermique = sum(recent_data.mapped('stress_thermique')) / len(recent_data)
                else:
                    record.stress_thermique = 0.0
            else:
                record.stress_thermique = 0.0

    @api.onchange('latitude', 'longitude')
    def _onchange_coordinates(self):
        if self.latitude and self.longitude:
            self.coordonnees_gps = f"{self.latitude:.6f}, {self.longitude:.6f}"
            self._calculer_surface_automatiquement()

    @api.onchange('geometrie_parcelle')
    def _onchange_geometrie(self):
        if self.geometrie_parcelle:
            self._calculer_surface_depuis_geometrie()

    def action_calculer_surface(self):
        """Calcule la surface de la parcelle"""
        self.ensure_one()
        if self.geometrie_parcelle:
            self._calculer_surface_depuis_geometrie()
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Surface Calculée',
                    'message': f'Surface calculée : {self.surface_calculee:.4f} hectares',
                    'type': 'success',
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Aucune Géométrie',
                    'message': 'Dessinez d\'abord la parcelle sur la carte',
                    'type': 'warning',
                }
            }

    def action_centrer_carte(self):
        """Centre la carte sur la parcelle"""
        self.ensure_one()
        if self.latitude and self.longitude:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Carte Centrée',
                    'message': f'Carte centrée sur {self.nom}',
                    'type': 'info',
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Coordonnées Manquantes',
                    'message': 'Ajoutez d\'abord les coordonnées GPS',
                    'type': 'warning',
                }
            }

    def _calculer_surface_depuis_geometrie(self):
        """Calcule la surface depuis les coordonnées géométriques"""
        try:
            if self.geometrie_parcelle:
                # Format attendu: "lat1,lng1;lat2,lng2;lat3,lng3;..."
                coords = self.geometrie_parcelle.split(';')
                if len(coords) >= 3:
                    points = []
                    for coord in coords:
                        if ',' in coord:
                            lat, lng = coord.strip().split(',')
                            points.append((float(lat), float(lng)))
                    
                    if len(points) >= 3:
                        # Calcul de l'aire avec la formule de Gauss
                        area = self._calculer_aire_polygone(points)
                        self.surface_calculee = area
                        self._update_exploitation_coordinates(points)
        except Exception as e:
            self.surface_calculee = 0.0

    def _calculer_aire_polygone(self, points):
        """Calcule l'aire d'un polygone avec la formule de Gauss"""
        n = len(points)
        area = 0.0
        
        for i in range(n):
            j = (i + 1) % n
            area += points[i][1] * points[j][0]  # lng * lat
            area -= points[j][1] * points[i][0]  # lng * lat
        
        area = abs(area) / 2.0
        
        # Conversion approximative en hectares
        # Facteur de conversion pour la latitude moyenne
        if points:
            lat_avg = sum(p[0] for p in points) / len(points)
            factor = 111.32 * 111.32 * abs(pow(0.0174533 * lat_avg, 0.5)) / 10000
            return area * factor
        
        return 0.0

    def _update_exploitation_coordinates(self, points):
        """Met à jour les coordonnées de l'exploitation si nécessaire"""
        if points and self.exploitation_id:
            # Calculer le centre de la parcelle
            center_lat = sum(p[0] for p in points) / len(points)
            center_lng = sum(p[1] for p in points) / len(points)
            
            # Mettre à jour les coordonnées de l'exploitation si elles sont vides
            if not self.exploitation_id.latitude or not self.exploitation_id.longitude:
                self.exploitation_id.write({
                    'latitude': center_lat,
                    'longitude': center_lng
                })

    def _calculer_surface_automatiquement(self):
        """Calcule automatiquement la surface si possible"""
        if self.latitude and self.longitude and not self.surface_calculee:
            # Surface par défaut basée sur la localisation
            # Cette méthode peut être améliorée avec des données satellitaires
            self.surface_calculee = 1.0  # 1 hectare par défaut

    @api.constrains('surface')
    def _check_surface_positive(self):
        for record in self:
            if record.surface and record.surface < 0:
                raise ValidationError("La surface doit être positive.")

    @api.constrains('ph_sol')
    def _check_ph_range(self):
        for record in self:
            if record.ph_sol and (record.ph_sol < 0 or record.ph_sol > 14):
                raise ValidationError("Le pH doit être entre 0 et 14.")

    @api.constrains('latitude', 'longitude')
    def _check_coordinates_range(self):
        for record in self:
            if record.latitude and (record.latitude < -90 or record.latitude > 90):
                raise ValidationError("La latitude doit être entre -90 et 90.")
            if record.longitude and (record.longitude < -180 or record.longitude > 180):
                raise ValidationError("La longitude doit être entre -180 et 180.")

    def action_activer(self):
        """Active la parcelle"""
        self.ensure_one()
        if self.state == 'draft':
            self.state = 'active'
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Parcelle Activée',
                    'message': f'La parcelle {self.nom} est maintenant active.',
                    'type': 'success',
                }
            }

    def action_archiver(self):
        """Archive la parcelle"""
        self.ensure_one()
        if self.state == 'active':
            self.state = 'archived'
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Parcelle Archivée',
                    'message': f'La parcelle {self.nom} a été archivée.',
                    'type': 'warning',
                }
            }

    def action_dupliquer(self):
        """Duplique la parcelle"""
        self.ensure_one()
        new_parcelle = self.copy({
            'nom': f"{self.nom} (Copie)",
            'state': 'draft',
            'geometrie_parcelle': False,
            'surface_calculee': 0.0
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'parcelle.agri',
            'res_id': new_parcelle.id,
            'view_mode': 'form',
            'target': 'current'
        }

    def name_get(self):
        """Personnalise l'affichage du nom"""
        result = []
        for record in self:
            name = f"{record.nom}"
            if record.exploitation_id:
                name += f" ({record.exploitation_id.nom})"
            result.append((record.id, name))
        return result


class ParcelleHistorique(models.Model):
    _name = 'parcelle.historique'
    _description = 'Historique des Parcelles'
    _order = 'date desc'

    parcelle_id = fields.Many2one('parcelle.agri', string="Parcelle", required=True, ondelete='cascade')
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    action = fields.Selection([
        ('creation', 'Création'),
        ('modification', 'Modification'),
        ('plantation', 'Plantation'),
        ('recolte', 'Récolte'),
        ('intervention', 'Intervention'),
        ('archivage', 'Archivage'),
    ], string="Action", required=True)
    details = fields.Text(string="Détails")
    utilisateur_id = fields.Many2one('res.users', string="Utilisateur", default=lambda self: self.env.user)
    anciennes_valeurs = fields.Text(string="Anciennes valeurs")
    nouvelles_valeurs = fields.Text(string="Nouvelles valeurs")

    @api.model
    def create(self, vals):
        """Crée automatiquement un historique lors de la création"""
        record = super().create(vals)
        if record.action == 'creation':
            record.details = f"Parcelle créée le {record.date}"
        return record 