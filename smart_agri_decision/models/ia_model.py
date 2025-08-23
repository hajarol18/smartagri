from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import json

class IAModel(models.Model):
    _name = 'ia.model'
    _description = 'Modèle d\'Intelligence Artificielle'
    _rec_name = 'name'
    _order = 'name'

    # Champs de base
    name = fields.Char(string="Nom du modèle", required=True)
    description = fields.Text(string="Description")
    type_modele = fields.Selection([
        ('regression', 'Régression'),
        ('classification', 'Classification'),
        ('clustering', 'Clustering'),
        ('series_temporelles', 'Séries temporelles'),
        ('deep_learning', 'Deep Learning'),
        ('ensemble', 'Ensemble Methods')
    ], string="Type de modèle", required=True, default='regression')
    
    algorithme = fields.Selection([
        ('linear_regression', 'Régression linéaire'),
        ('random_forest', 'Random Forest'),
        ('xgboost', 'XGBoost'),
        ('neural_network', 'Réseau de neurones'),
        ('svm', 'Support Vector Machine'),
        ('kmeans', 'K-Means'),
        ('lstm', 'LSTM'),
        ('transformer', 'Transformer')
    ], string="Algorithme", required=True, default='random_forest')
    
    # Relations
    exploitation_id = fields.Many2one('exploitation.agri', string="Exploitation", required=True)
    parcelle_id = fields.Many2one('parcelle.agri', string="Parcelle")
    
    # Configuration
    version = fields.Char(string="Version", default="1.0")
    auteur = fields.Char(string="Auteur")
    date_creation = fields.Datetime(string="Date de création", default=fields.Datetime.now, readonly=True)
    derniere_entrainement = fields.Datetime(string="Dernier entraînement")
    prochaine_entrainement = fields.Datetime(string="Prochain entraînement")
    
    # État
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('training', 'En entraînement'),
        ('trained', 'Entraîné'),
        ('active', 'Actif'),
        ('inactive', 'Inactif')
    ], string="État", default='draft', required=True)
    
    # Paramètres du modèle
    hyperparametres = fields.Text(string="Hyperparamètres (JSON)")
    seuil_confiance = fields.Float(string="Seuil de confiance", digits=(3, 2), default=0.8)
    taille_echantillon = fields.Integer(string="Taille échantillon", default=1000)
    
    # Données d'entraînement
    donnees_entrainement = fields.Integer(string="Données d'entraînement", default=0)
    donnees_validation = fields.Integer(string="Données de validation", default=0)
    donnees_test = fields.Integer(string="Données de test", default=0)
    qualite_donnees = fields.Selection([
        ('excellent', 'Excellent'),
        ('bon', 'Bon'),
        ('moyen', 'Moyen'),
        ('faible', 'Faible')
    ], string="Qualité des données", default='bon')
    
    # Performance
    precision = fields.Float(string="Précision (%)", digits=(5, 2))
    rappel = fields.Float(string="Rappel (%)", digits=(5, 2))
    f1_score = fields.Float(string="F1-Score (%)", digits=(5, 2))
    auc_score = fields.Float(string="AUC Score", digits=(4, 3))
    
    # Métriques
    erreur_moyenne = fields.Float(string="Erreur moyenne", digits=(6, 4))
    erreur_quadratique = fields.Float(string="Erreur quadratique", digits=(6, 4))
    coefficient_determination = fields.Float(string="Coefficient de détermination", digits=(4, 3))
    bias = fields.Float(string="Biais", digits=(6, 4))
    
    # Entraînement et validation
    nombre_entrainements = fields.Integer(string="Nombre d'entraînements", default=0)
    meilleur_score = fields.Float(string="Meilleur score", digits=(5, 2))
    evolution_performance = fields.Text(string="Évolution performance")
    overfitting_detected = fields.Boolean(string="Overfitting détecté", default=False)
    
    # Validation croisée
    folds_validation = fields.Integer(string="Folds validation", default=5)
    score_validation = fields.Float(string="Score validation", digits=(5, 2))
    ecart_type_validation = fields.Float(string="Écart-type validation", digits=(5, 2))
    
    # Prédictions
    derniere_prediction = fields.Datetime(string="Dernière prédiction")
    nombre_predictions = fields.Integer(string="Nombre de prédictions", default=0)
    taux_succes = fields.Float(string="Taux de succès (%)", digits=(5, 2))
    
    # Limites
    limites_prediction = fields.Text(string="Limites de prédiction")
    incertitude = fields.Float(string="Incertitude", digits=(5, 2))
    biais_connu = fields.Text(string="Biais connus")
    
    # Déploiement
    endpoint_api = fields.Char(string="Endpoint API")
    version_api = fields.Char(string="Version API")
    documentation_api = fields.Text(string="Documentation API")
    
    # Monitoring
    logs_prediction = fields.Text(string="Logs de prédiction")
    metriques_temps_reel = fields.Text(string="Métriques temps réel")
    alertes_performance = fields.Text(string="Alertes performance")
    
    # Intégration
    integrations = fields.Text(string="Intégrations")
    webhooks = fields.Text(string="Webhooks")
    format_sortie = fields.Selection([
        ('json', 'JSON'),
        ('xml', 'XML'),
        ('csv', 'CSV'),
        ('binary', 'Binaire')
    ], string="Format de sortie", default='json')
    
    # Sécurité
    authentification = fields.Selection([
        ('none', 'Aucune'),
        ('basic', 'Basic Auth'),
        ('token', 'Token'),
        ('oauth', 'OAuth2')
    ], string="Authentification", default='token')
    autorisation = fields.Text(string="Autorisation")
    chiffrement = fields.Selection([
        ('none', 'Aucun'),
        ('ssl', 'SSL/TLS'),
        ('aes', 'AES'),
        ('rsa', 'RSA')
    ], string="Chiffrement", default='ssl')
    
    # Relations One2many
    historique_entrainement_ids = fields.One2many('ia.historique.entrainement', 'modele_id', string="Historique d'entraînement")
    predictions_ids = fields.One2many('ia.prediction', 'modele_id', string="Prédictions")
    
    # Métadonnées
    create_date = fields.Datetime(string="Date de création", readonly=True)
    write_date = fields.Datetime(string="Dernière modification", readonly=True)
    create_uid = fields.Many2one('res.users', string="Créé par", readonly=True)
    write_uid = fields.Many2one('res.users', string="Modifié par", readonly=True)
    
    @api.constrains('seuil_confiance')
    def _check_seuil_confiance(self):
        for record in self:
            if record.seuil_confiance < 0 or record.seuil_confiance > 1:
                raise ValidationError("Le seuil de confiance doit être compris entre 0 et 1.")
    
    @api.constrains('taille_echantillon')
    def _check_taille_echantillon(self):
        for record in self:
            if record.taille_echantillon < 10:
                raise ValidationError("La taille d'échantillon doit être d'au moins 10.")
    
    def action_entrainer(self):
        """Lance l'entraînement du modèle"""
        self.ensure_one()
        if self.state in ['draft', 'inactive']:
            self.state = 'training'
            
            # Simuler l'entraînement (remplacé plus tard par l'IA réelle)
            self._simuler_entrainement()
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Entraînement Lancé',
                    'message': f'L\'entraînement du modèle {self.name} a commencé.',
                    'type': 'info',
                }
            }
    
    def _simuler_entrainement(self):
        """Simule l'entraînement du modèle (à remplacer par l'IA réelle)"""
        import random
        import time
        
        # Simuler un délai d'entraînement
        time.sleep(2)
        
        # Générer des métriques aléatoires
        self.precision = random.uniform(75, 95)
        self.rappel = random.uniform(70, 90)
        self.f1_score = random.uniform(72, 92)
        self.auc_score = random.uniform(0.7, 0.95)
        
        self.erreur_moyenne = random.uniform(0.05, 0.25)
        self.erreur_quadratique = random.uniform(0.1, 0.5)
        self.coefficient_determination = random.uniform(0.6, 0.9)
        self.bias = random.uniform(-0.2, 0.2)
        
        # Mettre à jour l'état
        self.state = 'trained'
        self.derniere_entrainement = datetime.now()
        self.nombre_entrainements += 1
        
        # Créer un historique d'entraînement
        self.env['ia.historique.entrainement'].create({
            'modele_id': self.id,
            'date_entrainement': datetime.now(),
            'precision': self.precision,
            'rappel': self.rappel,
            'f1_score': self.f1_score,
            'erreur_moyenne': self.erreur_moyenne,
            'duree_entrainement': random.uniform(30, 120),
            'commentaires': 'Entraînement simulé avec succès'
        })
    
    def action_activer(self):
        """Active le modèle pour les prédictions"""
        self.ensure_one()
        if self.state == 'trained':
            self.state = 'active'
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Modèle Activé',
                    'message': f'Le modèle {self.name} est maintenant actif pour les prédictions.',
                    'type': 'success',
                }
            }
    
    def action_desactiver(self):
        """Désactive le modèle"""
        self.ensure_one()
        if self.state == 'active':
            self.state = 'inactive'
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Modèle Désactivé',
                    'message': f'Le modèle {self.name} a été désactivé.',
                    'type': 'warning',
                }
            }
    
    def action_evaluer(self):
        """Évalue les performances du modèle"""
        self.ensure_one()
        if self.state == 'active':
            # Simuler une évaluation
            self._simuler_evaluation()
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Évaluation Terminée',
                    'message': f'L\'évaluation du modèle {self.name} a été effectuée.',
                    'type': 'success',
                }
            }
    
    def _simuler_evaluation(self):
        """Simule l'évaluation du modèle"""
        import random
        
        # Mettre à jour les métriques
        self.score_validation = random.uniform(70, 95)
        self.ecart_type_validation = random.uniform(2, 8)
        
        # Détecter l'overfitting
        if self.precision - self.score_validation > 10:
            self.overfitting_detected = True
        else:
            self.overfitting_detected = False
    
    def lancer_prediction(self, donnees_entree, parametres=None):
        """Lance une prédiction avec le modèle"""
        self.ensure_one()
        
        if self.state != 'active':
            raise ValidationError("Le modèle doit être actif pour lancer des prédictions.")
        
        # Créer une nouvelle prédiction
        prediction = self.env['ia.prediction'].create({
            'name': f"Prédiction {self.name} - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            'modele_id': self.id,
            'type_prediction': 'automatique',
            'donnees_entree': str(donnees_entree),
            'parametres': str(parametres) if parametres else '',
            'etat': 'en_cours'
        })
        
        # Simuler la prédiction
        prediction._simuler_prediction()
        
        # Mettre à jour les statistiques du modèle
        self.derniere_prediction = datetime.now()
        self.nombre_predictions += 1
        
        return prediction
    
    def calculer_metriques(self):
        """Calcule les métriques de performance du modèle"""
        self.ensure_one()
        
        if self.precision and self.rappel:
            # Calculer le F1-Score
            if self.precision + self.rappel > 0:
                self.f1_score = 2 * (self.precision * self.rappel) / (self.precision + self.rappel)
            else:
                self.f1_score = 0.0
        
        # Calculer le taux de succès basé sur les prédictions récentes
        predictions_recentes = self.env['ia.prediction'].search([
            ('modele_id', '=', self.id),
            ('etat', '=', 'validee')
        ], limit=100)
        
        if predictions_recentes:
            succes = sum(1 for p in predictions_recentes if p.precision > 0.8)
            self.taux_succes = (succes / len(predictions_recentes)) * 100
        else:
            self.taux_succes = 0.0


class IAHistoriqueEntrainement(models.Model):
    _name = 'ia.historique.entrainement'
    _description = 'Historique d\'entraînement IA'
    _order = 'date_entrainement desc'
    
    modele_id = fields.Many2one('ia.model', string="Modèle IA", required=True, ondelete='cascade')
    date_entrainement = fields.Datetime(string="Date d'entraînement", required=True)
    precision = fields.Float(string="Précision (%)", digits=(5, 2))
    rappel = fields.Float(string="Rappel (%)", digits=(5, 2))
    f1_score = fields.Float(string="F1-Score (%)", digits=(5, 2))
    erreur_moyenne = fields.Float(string="Erreur moyenne", digits=(6, 4))
    duree_entrainement = fields.Float(string="Durée d'entraînement (secondes)", digits=(8, 2))
    commentaires = fields.Text(string="Commentaires")
    
    _sql_constraints = [
        ('unique_entrainement_modele', 'unique(modele_id, date_entrainement)', 'Un entraînement ne peut être enregistré qu\'une fois par modèle et par date.')
    ]
