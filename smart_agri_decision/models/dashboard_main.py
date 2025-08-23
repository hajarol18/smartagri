from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import json

class DashboardMain(models.Model):
    _name = 'dashboard.main'
    _description = 'Tableau de Bord Principal'
    _rec_name = 'name'
    _order = 'name'

    # Champs de base
    name = fields.Char(string="Nom du tableau de bord", required=True)
    type_dashboard = fields.Selection([
        ('meteo', 'Météorologique'),
        ('agricole', 'Agricole'),
        ('economique', 'Économique'),
        ('environnemental', 'Environnemental'),
        ('global', 'Global')
    ], string="Type de tableau de bord", required=True, default='global')
    
    # Relations
    exploitation_id = fields.Many2one('exploitation.agri', string="Exploitation", required=True)
    
    # Configuration
    derniere_mise_a_jour = fields.Datetime(string="Dernière mise à jour", default=fields.Datetime.now)
    frequence_mise_a_jour = fields.Selection([
        ('realtime', 'Temps réel'),
        ('5min', '5 minutes'),
        ('15min', '15 minutes'),
        ('1h', '1 heure'),
        ('6h', '6 heures'),
        ('1j', '1 jour')
    ], string="Fréquence de mise à jour", default='15min')
    
    # Paramètres d'affichage
    theme = fields.Selection([
        ('light', 'Clair'),
        ('dark', 'Sombre'),
        ('auto', 'Automatique')
    ], string="Thème", default='light')
    
    langue = fields.Selection([
        ('fr_FR', 'Français'),
        ('en_US', 'English'),
        ('es_ES', 'Español')
    ], string="Langue", default='fr_FR')
    
    # Métadonnées
    create_date = fields.Datetime(string="Date de création", readonly=True)
    write_date = fields.Datetime(string="Dernière modification", readonly=True)
    create_uid = fields.Many2one('res.users', string="Créé par", readonly=True)
    write_uid = fields.Many2one('res.users', string="Modifié par", readonly=True)
    
    @api.constrains('frequence_mise_a_jour')
    def _check_frequence_mise_a_jour(self):
        for record in self:
            if record.frequence_mise_a_jour == 'realtime' and record.type_dashboard == 'global':
                raise ValidationError("La mise à jour temps réel n'est pas recommandée pour les tableaux de bord globaux.")
    
    def action_mettre_a_jour(self):
        """Met à jour le tableau de bord"""
        self.ensure_one()
        
        # Mettre à jour la date de dernière mise à jour
        self.derniere_mise_a_jour = datetime.now()
        
        # Déclencher la mise à jour selon le type
        if self.type_dashboard == 'meteo':
            self._mettre_a_jour_meteo()
        elif self.type_dashboard == 'agricole':
            self._mettre_a_jour_agricole()
        elif self.type_dashboard == 'global':
            self._mettre_a_jour_global()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Mise à jour effectuée',
                'message': f'Le tableau de bord {self.name} a été mis à jour.',
                'type': 'success',
            }
        }
    
    def _mettre_a_jour_meteo(self):
        """Met à jour les données météorologiques"""
        # Logique de mise à jour météo
        pass
    
    def _mettre_a_jour_agricole(self):
        """Met à jour les données agricoles"""
        # Logique de mise à jour agricole
        pass
    
    def _mettre_a_jour_global(self):
        """Met à jour toutes les données"""
        # Logique de mise à jour globale
        pass
    
    def generer_rapport(self, format_rapport='pdf'):
        """Génère un rapport du tableau de bord"""
        self.ensure_one()
        
        # Logique de génération de rapport
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Rapport généré',
                'message': f'Le rapport du tableau de bord {self.name} a été généré au format {format_rapport}.',
                'type': 'info',
            }
        }
    
    def exporter_donnees(self, format_export='csv'):
        """Exporte les données du tableau de bord"""
        self.ensure_one()
        
        # Logique d'export
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Export effectué',
                'message': f'Les données du tableau de bord {self.name} ont été exportées au format {format_export}.',
                'type': 'success',
            }
        }
    
    def planifier_mise_a_jour(self):
        """Planifie la prochaine mise à jour automatique"""
        self.ensure_one()
        
        # Calculer la prochaine mise à jour selon la fréquence
        maintenant = datetime.now()
        
        if self.frequence_mise_a_jour == '5min':
            prochaine = maintenant + timedelta(minutes=5)
        elif self.frequence_mise_a_jour == '15min':
            prochaine = maintenant + timedelta(minutes=15)
        elif self.frequence_mise_a_jour == '1h':
            prochaine = maintenant + timedelta(hours=1)
        elif self.frequence_mise_a_jour == '6h':
            prochaine = maintenant + timedelta(hours=6)
        elif self.frequence_mise_a_jour == '1j':
            prochaine = maintenant + timedelta(days=1)
        else:
            prochaine = maintenant
        
        return prochaine
    
    def obtenir_statistiques(self):
        """Retourne les statistiques du tableau de bord"""
        self.ensure_one()
        
        stats = {
            'nom': self.name,
            'type': self.type_dashboard,
            'derniere_mise_a_jour': self.derniere_mise_a_jour,
            'exploitation': self.exploitation_id.name if self.exploitation_id else 'N/A'
        }
        
        return stats
