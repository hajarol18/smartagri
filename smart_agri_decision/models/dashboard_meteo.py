from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import json

class DashboardMeteo(models.Model):
    _name = 'dashboard.meteo'
    _description = 'Tableau de Bord Météorologique'
    _rec_name = 'name'
    _order = 'name'

    # Champs de base
    name = fields.Char(string="Nom du tableau de bord", required=True)
    exploitation_id = fields.Many2one('exploitation.agri', string="Exploitation", required=True)
    
    # Configuration
    periode_analyse = fields.Selection([
        ('1j', '1 jour'),
        ('7j', '7 jours'),
        ('30j', '30 jours'),
        ('90j', '90 jours'),
        ('1an', '1 an')
    ], string="Période d'analyse", default='7j', required=True)
    
    derniere_mise_a_jour = fields.Datetime(string="Dernière mise à jour", default=fields.Datetime.now)
    prochaine_mise_a_jour = fields.Datetime(string="Prochaine mise à jour")
    
    # Paramètres d'affichage
    unite_temperature = fields.Selection([
        ('celsius', 'Celsius'),
        ('fahrenheit', 'Fahrenheit'),
        ('kelvin', 'Kelvin')
    ], string="Unité température", default='celsius')
    
    unite_precipitation = fields.Selection([
        ('mm', 'Millimètres'),
        ('cm', 'Centimètres'),
        ('inch', 'Pouces')
    ], string="Unité précipitations", default='mm')
    
    langue = fields.Selection([
        ('fr_FR', 'Français'),
        ('en_US', 'English'),
        ('es_ES', 'Español')
    ], string="Langue", default='fr_FR')
    
    theme = fields.Selection([
        ('light', 'Clair'),
        ('dark', 'Sombre'),
        ('auto', 'Automatique')
    ], string="Thème", default='light')
    
    # Vue d'ensemble - Conditions actuelles
    temperature_actuelle = fields.Float(string="Température actuelle (°C)", digits=(4, 1))
    humidite_actuelle = fields.Float(string="Humidité actuelle (%)", digits=(4, 1))
    precipitation_actuelle = fields.Float(string="Précipitations actuelles (mm)", digits=(5, 2))
    vent_actuel = fields.Float(string="Vitesse du vent (km/h)", digits=(4, 1))
    
    # Vue d'ensemble - Tendances
    tendance_temperature = fields.Selection([
        ('hausse', 'Hausse'),
        ('stable', 'Stable'),
        ('baisse', 'Baisse')
    ], string="Tendance température")
    
    tendance_precipitation = fields.Selection([
        ('augmentation', 'Augmentation'),
        ('stable', 'Stable'),
        ('diminution', 'Diminution')
    ], string="Tendance précipitations")
    
    tendance_humidite = fields.Selection([
        ('augmentation', 'Augmentation'),
        ('stable', 'Stable'),
        ('diminution', 'Diminution')
    ], string="Tendance humidité")
    
    tendance_vent = fields.Selection([
        ('augmentation', 'Augmentation'),
        ('stable', 'Stable'),
        ('diminution', 'Diminution')
    ], string="Tendance vent")
    
    # Vue d'ensemble - Alertes actives
    alertes_actives_count = fields.Integer(string="Nombre d'alertes actives", default=0)
    niveau_alerte_max = fields.Selection([
        ('vert', 'Vert'),
        ('jaune', 'Jaune'),
        ('orange', 'Orange'),
        ('rouge', 'Rouge')
    ], string="Niveau d'alerte max", default='vert')
    
    derniere_alerte = fields.Datetime(string="Dernière alerte")
    
    # Vue d'ensemble - Indices
    indice_uv = fields.Integer(string="Indice UV", default=0)
    indice_qualite_air = fields.Selection([
        ('excellent', 'Excellent'),
        ('bon', 'Bon'),
        ('moyen', 'Moyen'),
        ('mauvais', 'Mauvais'),
        ('tres_mauvais', 'Très mauvais')
    ], string="Indice qualité air", default='bon')
    
    indice_confort = fields.Selection([
        ('excellent', 'Excellent'),
        ('bon', 'Bon'),
        ('moyen', 'Moyen'),
        ('mauvais', 'Mauvais'),
        ('tres_mauvais', 'Très mauvais')
    ], string="Indice confort", default='bon')
    
    # Prévisions - Court terme (7 jours)
    previsions_7j = fields.Text(string="Prévisions 7 jours")
    confiance_previsions = fields.Float(string="Confiance prévisions (%)", digits=(5, 2))
    source_previsions = fields.Char(string="Source prévisions")
    
    # Prévisions - Saisonnières
    previsions_saisonnières = fields.Text(string="Prévisions saisonnières")
    anomalies_climatiques = fields.Text(string="Anomalies climatiques")
    risques_climatiques = fields.Text(string="Risques climatiques")
    
    # Analyses - Statistiques
    temperature_moyenne = fields.Float(string="Température moyenne (°C)", digits=(4, 1))
    temperature_min = fields.Float(string="Température minimale (°C)", digits=(4, 1))
    temperature_max = fields.Float(string="Température maximale (°C)", digits=(4, 1))
    precipitation_totale = fields.Float(string="Précipitations totales (mm)", digits=(6, 2))
    
    # Analyses - Records
    record_temperature_max = fields.Float(string="Record température max (°C)", digits=(4, 1))
    record_temperature_min = fields.Float(string="Record température min (°C)", digits=(4, 1))
    record_precipitation = fields.Float(string="Record précipitations (mm)", digits=(6, 2))
    record_vent = fields.Float(string="Record vent (km/h)", digits=(4, 1))
    
    # Cartes interactives
    graphique_previsions = fields.Binary(string="Graphique prévisions")
    graphique_statistiques = fields.Binary(string="Graphique statistiques")
    carte_meteo = fields.Binary(string="Carte météo")
    carte_alertes = fields.Binary(string="Carte des alertes")
    carte_stations = fields.Binary(string="Carte des stations")
    carte_parcelles = fields.Binary(string="Carte des parcelles")
    
    # Configuration des cartes
    zoom_carte = fields.Integer(string="Zoom carte", default=10)
    centre_carte = fields.Char(string="Centre carte")
    filtres_alertes = fields.Text(string="Filtres alertes")
    stations_actives = fields.Integer(string="Stations actives", default=0)
    parcelles_surveillees = fields.Integer(string="Parcelles surveillées", default=0)
    
    # Rapports
    rapport_quotidien = fields.Boolean(string="Rapport quotidien", default=True)
    rapport_hebdomadaire = fields.Boolean(string="Rapport hebdomadaire", default=True)
    rapport_mensuel = fields.Boolean(string="Rapport mensuel", default=True)
    rapport_saisonnier = fields.Boolean(string="Rapport saisonnier", default=True)
    
    format_export = fields.Selection([
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
        ('json', 'JSON')
    ], string="Format export", default='pdf')
    
    frequence_export = fields.Selection([
        ('manuel', 'Manuel'),
        ('quotidien', 'Quotidien'),
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuel', 'Mensuel')
    ], string="Fréquence export", default='manuel')
    
    destinataires = fields.Text(string="Destinataires")
    
    # Relations One2many
    derniers_rapports_ids = fields.One2many('dashboard.rapport', 'dashboard_id', string="Derniers rapports")
    
    # Métadonnées
    create_date = fields.Datetime(string="Date de création", readonly=True)
    write_date = fields.Datetime(string="Dernière modification", readonly=True)
    create_uid = fields.Many2one('res.users', string="Créé par", readonly=True)
    write_uid = fields.Many2one('res.users', string="Modifié par", readonly=True)
    
    @api.constrains('confiance_previsions')
    def _check_confiance_previsions(self):
        for record in self:
            if record.confiance_previsions and (record.confiance_previsions < 0 or record.confiance_previsions > 100):
                raise ValidationError("La confiance des prévisions doit être comprise entre 0 et 100%.")
    
    @api.constrains('zoom_carte')
    def _check_zoom_carte(self):
        for record in self:
            if record.zoom_carte < 1 or record.zoom_carte > 20:
                raise ValidationError("Le zoom de la carte doit être compris entre 1 et 20.")
    
    def action_mettre_a_jour_meteo(self):
        """Met à jour les données météorologiques"""
        self.ensure_one()
        
        # Mettre à jour la date de dernière mise à jour
        self.derniere_mise_a_jour = datetime.now()
        
        # Récupérer les données météo actuelles
        self._recuperer_donnees_actuelles()
        
        # Calculer les tendances
        self._calculer_tendances()
        
        # Vérifier les alertes
        self._verifier_alertes()
        
        # Mettre à jour les statistiques
        self._mettre_a_jour_statistiques()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Mise à jour météo',
                'message': f'Les données météorologiques ont été mises à jour pour {self.exploitation_id.name}.',
                'type': 'success',
            }
        }
    
    def _recuperer_donnees_actuelles(self):
        """Récupère les données météo actuelles"""
        # Récupérer les dernières données météo de l'exploitation
        derniere_meteo = self.env['meteo.data'].search([
            ('exploitation_id', '=', self.exploitation_id.id)
        ], order='date desc', limit=1)
        
        if derniere_meteo:
            self.temperature_actuelle = derniere_meteo.temperature
            self.humidite_actuelle = derniere_meteo.humidite
            self.precipitation_actuelle = derniere_meteo.precipitation
            self.vent_actuel = derniere_meteo.vent_vitesse
    
    def _calculer_tendances(self):
        """Calcule les tendances météorologiques"""
        # Logique de calcul des tendances
        # À implémenter avec des algorithmes de détection de tendances
        pass
    
    def _verifier_alertes(self):
        """Vérifie et met à jour les alertes météo"""
        # Compter les alertes actives avec un domaine correctement formé
        alertes = self.env['meteo.data'].search([
            ('exploitation_id', '=', self.exploitation_id.id),
            '|',
            '|',
            '|',
            '|',
            ('alerte_gel', '=', True),
            ('alerte_canicule', '=', True),
            ('alerte_secheresse', '=', True),
            ('alerte_inondation', '=', True),
            ('alerte_vent', '=', True)
        ])
        
        self.alertes_actives_count = len(alertes)
        
        # Déterminer le niveau d'alerte max
        if alertes:
            niveaux = {'vert': 0, 'jaune': 1, 'orange': 2, 'rouge': 3}
            niveau_max = 'vert'
            
            for alerte in alertes:
                # Logique de détermination du niveau d'alerte
                pass
            
            self.niveau_alerte_max = niveau_max
            self.derniere_alerte = datetime.now()
    
    def _mettre_a_jour_statistiques(self):
        """Met à jour les statistiques météorologiques"""
        # Calculer les moyennes, min, max sur la période
        date_debut = datetime.now() - timedelta(days=self._get_periode_jours())
        
        donnees_periode = self.env['meteo.data'].search([
            ('exploitation_id', '=', self.exploitation_id.id),
            ('date', '>=', date_debut)
        ])
        
        if donnees_periode:
            temperatures = [d.temperature for d in donnees_periode if d.temperature]
            precipitations = [d.precipitation for d in donnees_periode if d.precipitation]
            
            if temperatures:
                self.temperature_moyenne = sum(temperatures) / len(temperatures)
                self.temperature_min = min(temperatures)
                self.temperature_max = max(temperatures)
            
            if precipitations:
                self.precipitation_totale = sum(precipitations)
    
    def _get_periode_jours(self):
        """Retourne le nombre de jours selon la période sélectionnée"""
        mapping = {
            '1j': 1,
            '7j': 7,
            '30j': 30,
            '90j': 90,
            '1an': 365
        }
        return mapping.get(self.periode_analyse, 7)
    
    def generer_rapport_meteo(self, type_rapport='quotidien'):
        """Génère un rapport météorologique"""
        self.ensure_one()
        
        # Créer un nouveau rapport
        rapport = self.env['dashboard.rapport'].create({
            'dashboard_id': self.id,
            'type_rapport': type_rapport,
            'date_rapport': datetime.now(),
            'statut': 'en_cours'
        })
        
        # Générer le contenu du rapport
        rapport._generer_contenu_meteo()
        
        return rapport
    
    def obtenir_resume_meteo(self):
        """Retourne un résumé météorologique"""
        self.ensure_one()
        
        resume = {
            'temperature': f"{self.temperature_actuelle:.1f}°C" if self.temperature_actuelle else "N/A",
            'humidite': f"{self.humidite_actuelle:.1f}%" if self.humidite_actuelle else "N/A",
            'precipitation': f"{self.precipitation_actuelle:.1f}mm" if self.precipitation_actuelle else "N/A",
            'vent': f"{self.vent_actuel:.1f}km/h" if self.vent_actuel else "N/A",
            'alertes': self.alertes_actives_count,
            'niveau_alerte': self.niveau_alerte_max
        }
        
        return resume


class DashboardRapport(models.Model):
    _name = 'dashboard.rapport'
    _description = 'Rapport de Tableau de Bord'
    _order = 'date_rapport desc'
    
    dashboard_id = fields.Many2one('dashboard.meteo', string="Tableau de bord", required=True, ondelete='cascade')
    type_rapport = fields.Selection([
        ('quotidien', 'Quotidien'),
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuel', 'Mensuel'),
        ('saisonnier', 'Saisonnier')
    ], string="Type de rapport", required=True)
    
    date_rapport = fields.Datetime(string="Date du rapport", required=True)
    statut = fields.Selection([
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('erreur', 'Erreur')
    ], string="Statut", default='en_cours')
    
    taille_fichier = fields.Char(string="Taille fichier")
    actions = fields.Text(string="Actions")
    
    def _generer_contenu_meteo(self):
        """Génère le contenu du rapport météo"""
        self.ensure_one()
        
        # Logique de génération du contenu
        self.statut = 'termine'
        self.taille_fichier = '2.5 MB'
        self.actions = 'Rapport généré avec succès'
