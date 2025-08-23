from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import json

class IAPrediction(models.Model):
    _name = 'ia.prediction'
    _description = 'Prédiction IA'
    _rec_name = 'name'
    _order = 'date_prediction desc'

    # Champs de base
    name = fields.Char(string="Nom de la prédiction", required=True)
    modele_id = fields.Many2one('ia.model', string="Modèle IA", required=True)
    type_prediction = fields.Selection([
        ('rendement', 'Rendement'),
        ('stress', 'Stress'),
        ('irrigation', 'Irrigation'),
        ('fertilisation', 'Fertilisation'),
        ('recolte', 'Récolte'),
        ('risque', 'Risque'),
        ('automatique', 'Automatique')
    ], string="Type de prédiction", required=True, default='rendement')
    
    description = fields.Text(string="Description")
    priorite = fields.Selection([
        ('basse', 'Basse'),
        ('normale', 'Normale'),
        ('haute', 'Haute'),
        ('critique', 'Critique')
    ], string="Priorité", default='normale')
    
    # Données d'entrée
    donnees_entree = fields.Text(string="Données d'entrée")
    parametres = fields.Text(string="Paramètres")
    contraintes = fields.Text(string="Contraintes")
    
    # État
    etat = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('validee', 'Validée'),
        ('rejetee', 'Rejetée'),
        ('erreur', 'Erreur')
    ], string="État", default='brouillon', required=True)
    
    # Résultats
    valeur_predite = fields.Float(string="Valeur prédite", digits=(10, 4))
    confiance = fields.Float(string="Confiance (%)", digits=(5, 2))
    intervalle_confiance = fields.Char(string="Intervalle de confiance")
    marge_erreur = fields.Float(string="Marge d'erreur", digits=(6, 4))
    
    # Métriques
    score_qualite = fields.Float(string="Score de qualité", digits=(4, 2))
    anomalies_detectees = fields.Text(string="Anomalies détectées")
    explications = fields.Text(string="Explications")
    
    # Validation
    valeur_reelle = fields.Float(string="Valeur réelle", digits=(10, 4))
    erreur = fields.Float(string="Erreur", digits=(10, 4))
    precision = fields.Float(string="Précision (%)", digits=(5, 2))
    commentaires_validation = fields.Text(string="Commentaires de validation")
    
    # Actions
    actions_recommandees = fields.Text(string="Actions recommandées")
    risques_identifies = fields.Text(string="Risques identifiés")
    opportunites = fields.Text(string="Opportunités")
    
    # Historique d'exécution
    historique_execution_ids = fields.One2many('ia.historique.execution', 'prediction_id', string="Historique d'exécution")
    
    # Métadonnées
    date_prediction = fields.Datetime(string="Date de prédiction", default=fields.Datetime.now)
    create_date = fields.Datetime(string="Date de création", readonly=True)
    write_date = fields.Datetime(string="Dernière modification", readonly=True)
    create_uid = fields.Many2one('res.users', string="Créé par", readonly=True)
    write_uid = fields.Many2one('res.users', string="Modifié par", readonly=True)
    
    @api.constrains('confiance')
    def _check_confiance(self):
        for record in self:
            if record.confiance and (record.confiance < 0 or record.confiance > 100):
                raise ValidationError("La confiance doit être comprise entre 0 et 100%.")
    
    @api.constrains('priorite')
    def _check_priorite(self):
        for record in self:
            if record.priorite == 'critique' and record.etat == 'brouillon':
                raise ValidationError("Une prédiction critique ne peut rester en brouillon.")
    
    def action_lancer_prediction(self):
        """Lance la prédiction avec le modèle sélectionné"""
        self.ensure_one()
        
        if self.etat != 'brouillon':
            raise ValidationError("Seules les prédictions en brouillon peuvent être lancées.")
        
        if not self.modele_id:
            raise ValidationError("Un modèle IA doit être sélectionné.")
        
        if self.modele_id.state != 'active':
            raise ValidationError("Le modèle sélectionné doit être actif.")
        
        # Mettre à jour l'état
        self.etat = 'en_cours'
        
        # Créer un historique d'exécution
        self.env['ia.historique.execution'].create({
            'prediction_id': self.id,
            'date_execution': datetime.now(),
            'etat': 'en_cours',
            'commentaires': 'Prédiction lancée'
        })
        
        # Simuler la prédiction
        self._simuler_prediction()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Prédiction Lancée',
                'message': f'La prédiction {self.name} a été lancée avec le modèle {self.modele_id.name}.',
                'type': 'info',
            }
        }
    
    def _simuler_prediction(self):
        """Simule la prédiction (à remplacer par l'IA réelle)"""
        import random
        import time
        
        # Simuler un délai de traitement
        time.sleep(1)
        
        # Générer des valeurs simulées selon le type de prédiction
        if self.type_prediction == 'rendement':
            self.valeur_predite = random.uniform(80, 120)  # tonnes/ha
            self.confiance = random.uniform(75, 95)
        elif self.type_prediction == 'stress':
            self.valeur_predite = random.uniform(0, 1)  # indice 0-1
            self.confiance = random.uniform(80, 98)
        elif self.type_prediction == 'irrigation':
            self.valeur_predite = random.uniform(20, 80)  # mm
            self.confiance = random.uniform(70, 90)
        else:
            self.valeur_predite = random.uniform(50, 150)
            self.confiance = random.uniform(75, 95)
        
        # Calculer l'intervalle de confiance
        marge = self.valeur_predite * (1 - self.confiance / 100) * 0.1
        self.marge_erreur = marge
        self.intervalle_confiance = f"{self.valeur_predite - marge:.2f} - {self.valeur_predite + marge:.2f}"
        
        # Score de qualité basé sur la confiance
        self.score_qualite = self.confiance / 100
        
        # Détecter des anomalies
        if self.confiance < 80:
            self.anomalies_detectees = "Confiance faible détectée"
        else:
            self.anomalies_detectees = "Aucune anomalie détectée"
        
        # Générer des explications
        self.explications = f"Prédiction basée sur le modèle {self.modele_id.name} avec {self.confiance:.1f}% de confiance."
        
        # Actions recommandées
        if self.type_prediction == 'rendement' and self.valeur_predite < 90:
            self.actions_recommandees = "Augmenter la fertilisation et l'irrigation"
        elif self.type_prediction == 'stress' and self.valeur_predite > 0.7:
            self.actions_recommandees = "Intervention urgente requise"
        else:
            self.actions_recommandees = "Maintenir les pratiques actuelles"
        
        # Mettre à jour l'état
        self.etat = 'terminee'
        
        # Mettre à jour l'historique
        historique = self.env['ia.historique.execution'].search([
            ('prediction_id', '=', self.id),
            ('etat', '=', 'en_cours')
        ], limit=1)
        
        if historique:
            historique.write({
                'etat': 'terminee',
                'duree_execution': random.uniform(5, 30),
                'ressources_utilisees': 'CPU: 15%, RAM: 512MB',
                'commentaires': 'Prédiction terminée avec succès'
            })
    
    def action_valider(self):
        """Valide la prédiction"""
        self.ensure_one()
        
        if self.etat != 'terminee':
            raise ValidationError("Seules les prédictions terminées peuvent être validées.")
        
        self.etat = 'validee'
        
        # Créer un historique de validation
        self.env['ia.historique.execution'].create({
            'prediction_id': self.id,
            'date_execution': datetime.now(),
            'etat': 'validee',
            'commentaires': 'Prédiction validée par l\'utilisateur'
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Prédiction Validée',
                'message': f'La prédiction {self.name} a été validée.',
                'type': 'success',
            }
        }
    
    def action_rejeter(self):
        """Rejette la prédiction"""
        self.ensure_one()
        
        if self.etat != 'terminee':
            raise ValidationError("Seules les prédictions terminées peuvent être rejetées.")
        
        self.etat = 'rejetee'
        
        # Créer un historique de rejet
        self.env['ia.historique.execution'].create({
            'prediction_id': self.id,
            'date_execution': datetime.now(),
            'etat': 'rejetee',
            'commentaires': 'Prédiction rejetée par l\'utilisateur'
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Prédiction Rejetée',
                'message': f'La prédiction {self.name} a été rejetée.',
                'type': 'warning',
            }
        }
    
    def saisir_valeur_reelle(self, valeur):
        """Saisit la valeur réelle pour calculer l'erreur"""
        self.ensure_one()
        
        if not self.valeur_predite:
            raise ValidationError("La prédiction doit d'abord être terminée.")
        
        self.valeur_reelle = valeur
        self.erreur = abs(self.valeur_predite - self.valeur_reelle)
        
        # Calculer la précision
        if self.valeur_reelle != 0:
            self.precision = max(0, 100 - (self.erreur / abs(self.valeur_reelle) * 100))
        else:
            self.precision = 0 if self.erreur > 0 else 100
        
        # Mettre à jour les métriques du modèle
        if self.modele_id:
            self.modele_id.calculer_metriques()
    
    def calculer_qualite(self):
        """Calcule la qualité de la prédiction"""
        self.ensure_one()
        
        if not self.valeur_predite or not self.valeur_reelle:
            return
        
        # Calculer l'erreur relative
        erreur_relative = abs(self.valeur_predite - self.valeur_reelle) / abs(self.valeur_reelle) * 100
        
        # Ajuster le score de qualité
        if erreur_relative < 5:
            self.score_qualite = 1.0
        elif erreur_relative < 10:
            self.score_qualite = 0.8
        elif erreur_relative < 20:
            self.score_qualite = 0.6
        else:
            self.score_qualite = 0.4


class IAHistoriqueExecution(models.Model):
    _name = 'ia.historique.execution'
    _description = 'Historique d\'exécution IA'
    _order = 'date_execution desc'
    
    prediction_id = fields.Many2one('ia.prediction', string="Prédiction IA", required=True, ondelete='cascade')
    date_execution = fields.Datetime(string="Date d'exécution", required=True)
    etat = fields.Selection([
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('validee', 'Validée'),
        ('rejetee', 'Rejetée'),
        ('erreur', 'Erreur')
    ], string="État", required=True)
    duree_execution = fields.Float(string="Durée d'exécution (secondes)", digits=(8, 2))
    ressources_utilisees = fields.Char(string="Ressources utilisées")
    logs = fields.Text(string="Logs d'exécution")
    commentaires = fields.Text(string="Commentaires")
    
    _sql_constraints = [
        ('unique_execution_prediction', 'unique(prediction_id, date_execution)', 'Une exécution ne peut être enregistrée qu\'une fois par prédiction et par date.')
    ]
