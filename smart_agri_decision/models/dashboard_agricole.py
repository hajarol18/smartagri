from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import json

class DashboardAgricole(models.Model):
    _name = 'dashboard.agricole'
    _description = 'Tableau de Bord Agricole'
    _rec_name = 'name'
    _order = 'name'

    # Champs de base
    name = fields.Char(string="Nom du tableau de bord agricole", required=True)
    exploitation_id = fields.Many2one('exploitation.agri', string="Exploitation", required=True)
    
    # Exploitation
    superficie_totale = fields.Float(string="Superficie totale (ha)", digits=(8, 2))
    nombre_parcelles = fields.Integer(string="Nombre de parcelles", default=0)
    type_cultures = fields.Text(string="Types de cultures")
    
    # Saison
    saison_courante = fields.Selection([
        ('printemps', 'Printemps'),
        ('ete', 'Été'),
        ('automne', 'Automne'),
        ('hiver', 'Hiver')
    ], string="Saison courante")
    
    phase_culture = fields.Selection([
        ('preparation', 'Préparation'),
        ('semis', 'Semis'),
        ('levée', 'Levée'),
        ('croissance', 'Croissance'),
        ('floraison', 'Floraison'),
        ('fructification', 'Fructification'),
        ('maturite', 'Maturité'),
        ('recolte', 'Récolte')
    ], string="Phase de culture")
    
    jours_apres_semis = fields.Integer(string="Jours après semis", default=0)
    prochaine_intervention = fields.Datetime(string="Prochaine intervention")
    
    # Rendements
    rendement_actuel = fields.Float(string="Rendement actuel (t/ha)", digits=(6, 2))
    rendement_precedent = fields.Float(string="Rendement précédent (t/ha)", digits=(6, 2))
    evolution_rendement = fields.Float(string="Évolution rendement (%)", digits=(5, 2))
    objectif_rendement = fields.Float(string="Objectif rendement (t/ha)", digits=(6, 2))
    
    # Prédictions
    rendement_predit = fields.Float(string="Rendement prédit (t/ha)", digits=(6, 2))
    confiance_prediction = fields.Float(string="Confiance prédiction (%)", digits=(5, 2))
    facteurs_risque = fields.Text(string="Facteurs de risque")
    opportunites_amelioration = fields.Text(string="Opportunités d'amélioration")
    
    # Interventions
    interventions_planifiees = fields.Integer(string="Interventions planifiées", default=0)
    cout_interventions = fields.Float(string="Coût interventions (€)", digits=(10, 2))
    priorite_interventions = fields.Selection([
        ('basse', 'Basse'),
        ('normale', 'Normale'),
        ('haute', 'Haute'),
        ('critique', 'Critique')
    ], string="Priorité interventions", default='normale')
    
    interventions_realisees = fields.Integer(string="Interventions réalisées", default=0)
    efficacite_interventions = fields.Float(string="Efficacité interventions (%)", digits=(5, 2))
    retour_investissement = fields.Float(string="Retour investissement (%)", digits=(5, 2))
    
    # Ressources - Eau
    consommation_eau = fields.Float(string="Consommation eau (m³/ha)", digits=(8, 2))
    disponibilite_eau = fields.Float(string="Disponibilité eau (m³/ha)", digits=(8, 2))
    efficacite_irrigation = fields.Float(string="Efficacité irrigation (%)", digits=(5, 2))
    stress_hydrique = fields.Float(string="Stress hydrique (0-1)", digits=(3, 2))
    
    # Ressources - Nutriments
    azote_sol = fields.Float(string="Azote sol (kg/ha)", digits=(6, 2))
    phosphore_sol = fields.Float(string="Phosphore sol (kg/ha)", digits=(6, 2))
    potassium_sol = fields.Float(string="Potassium sol (kg/ha)", digits=(6, 2))
    ph_sol = fields.Float(string="pH sol", digits=(3, 1))
    
    # Ressources - Énergie
    consommation_energie = fields.Float(string="Consommation énergie (kWh/ha)", digits=(8, 2))
    sources_energie = fields.Selection([
        ('fossile', 'Fossile'),
        ('renouvelable', 'Renouvelable'),
        ('mixte', 'Mixte')
    ], string="Sources d'énergie", default='mixte')
    
    efficacite_energetique = fields.Float(string="Efficacité énergétique (%)", digits=(5, 2))
    
    # Ressources - Main d'œuvre
    heures_travail = fields.Float(string="Heures de travail (h/ha)", digits=(6, 2))
    productivite_travail = fields.Float(string="Productivité travail (€/h)", digits=(6, 2))
    cout_main_oeuvre = fields.Float(string="Coût main d'œuvre (€/ha)", digits=(8, 2))
    
    # Qualité
    indice_qualite = fields.Float(string="Indice qualité (0-100)", digits=(5, 2))
    conformite_standards = fields.Float(string="Conformité standards (%)", digits=(5, 2))
    defauts_detectes = fields.Text(string="Défauts détectés")
    satisfaction_clients = fields.Float(string="Satisfaction clients (%)", digits=(5, 2))
    
    # Certifications
    certifications_obtenues = fields.Text(string="Certifications obtenues")
    audits_realises = fields.Integer(string="Audits réalisés", default=0)
    conformite_reglementaire = fields.Float(string="Conformité réglementaire (%)", digits=(5, 2))
    
    # Durabilité - Impact environnemental
    emissions_co2 = fields.Float(string="Émissions CO2 (kg/ha)", digits=(8, 2))
    utilisation_pesticides = fields.Float(string="Utilisation pesticides (kg/ha)", digits=(6, 2))
    gestion_dechets = fields.Selection([
        ('excellent', 'Excellent'),
        ('bon', 'Bon'),
        ('moyen', 'Moyen'),
        ('mauvais', 'Mauvais')
    ], string="Gestion déchets", default='bon')
    
    biodiversite = fields.Float(string="Indice biodiversité (0-100)", digits=(5, 2))
    
    # Durabilité - Pratiques durables
    agriculture_conservation = fields.Boolean(string="Agriculture de conservation", default=False)
    rotation_cultures = fields.Boolean(string="Rotation des cultures", default=True)
    couverture_sol = fields.Boolean(string="Couverture du sol", default=False)
    gestion_integree = fields.Boolean(string="Gestion intégrée", default=True)
    
    # Graphiques et indicateurs
    graphique_rendements = fields.Binary(string="Graphique rendements")
    graphique_qualite = fields.Binary(string="Graphique qualité")
    calendrier_interventions = fields.Binary(string="Calendrier interventions")
    indicateurs_durabilite = fields.Binary(string="Indicateurs durabilité")
    
    # Métadonnées
    create_date = fields.Datetime(string="Date de création", readonly=True)
    write_date = fields.Datetime(string="Dernière modification", readonly=True)
    create_uid = fields.Many2one('res.users', string="Créé par", readonly=True)
    write_uid = fields.Many2one('res.users', string="Modifié par", readonly=True)
    
    @api.constrains('confiance_prediction')
    def _check_confiance_prediction(self):
        for record in self:
            if record.confiance_prediction and (record.confiance_prediction < 0 or record.confiance_prediction > 100):
                raise ValidationError("La confiance de prédiction doit être comprise entre 0 et 100%.")
    
    @api.constrains('stress_hydrique')
    def _check_stress_hydrique(self):
        for record in self:
            if record.stress_hydrique and (record.stress_hydrique < 0 or record.stress_hydrique > 1):
                raise ValidationError("Le stress hydrique doit être compris entre 0 et 1.")
    
    @api.constrains('ph_sol')
    def _check_ph_sol(self):
        for record in self:
            if record.ph_sol and (record.ph_sol < 0 or record.ph_sol > 14):
                raise ValidationError("Le pH du sol doit être compris entre 0 et 14.")
    
    @api.onchange('exploitation_id')
    def _onchange_exploitation_id(self):
        """Met à jour les informations de l'exploitation"""
        if self.exploitation_id:
            # Calculer la superficie totale
            parcelles = self.env['parcelle.agri'].search([
                ('exploitation_id', '=', self.exploitation_id.id)
            ])
            
            self.superficie_totale = sum(parcelle.superficie for parcelle in parcelles)
            self.nombre_parcelles = len(parcelles)
            
            # Déterminer les types de cultures
            cultures = set()
            for parcelle in parcelles:
                if parcelle.culture_id:
                    cultures.add(parcelle.culture_id.nom)
            
            self.type_cultures = ', '.join(cultures) if cultures else 'Aucune culture'
    
    def action_mettre_a_jour_agricole(self):
        """Met à jour le tableau de bord agricole"""
        self.ensure_one()
        
        # Mettre à jour les informations de l'exploitation
        self._mettre_a_jour_exploitation()
        
        # Mettre à jour les rendements
        self._mettre_a_jour_rendements()
        
        # Mettre à jour les interventions
        self._mettre_a_jour_interventions()
        
        # Mettre à jour les ressources
        self._mettre_a_jour_ressources()
        
        # Mettre à jour la qualité
        self._mettre_a_jour_qualite()
        
        # Mettre à jour la durabilité
        self._mettre_a_jour_durabilite()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Mise à jour agricole',
                'message': f'Le tableau de bord agricole a été mis à jour pour {self.exploitation_id.name}.',
                'type': 'success',
            }
        }
    
    def _mettre_a_jour_exploitation(self):
        """Met à jour les informations de l'exploitation"""
        # Déterminer la saison courante
        mois = datetime.now().month
        if mois in [3, 4, 5]:
            self.saison_courante = 'printemps'
        elif mois in [6, 7, 8]:
            self.saison_courante = 'ete'
        elif mois in [9, 10, 11]:
            self.saison_courante = 'automne'
        else:
            self.saison_courante = 'hiver'
        
        # Calculer les jours après semis (simulation)
        if self.saison_courante in ['printemps', 'ete']:
            self.jours_apres_semis = (datetime.now() - datetime(2024, 3, 15)).days
        else:
            self.jours_apres_semis = 0
    
    def _mettre_a_jour_rendements(self):
        """Met à jour les informations de rendement"""
        # Récupérer le dernier rendement enregistré
        dernier_rendement = self.env['rendement.agri'].search([
            ('parcelle_id.exploitation_id', '=', self.exploitation_id.id)
        ], order='date_recolte desc', limit=1)
        
        if dernier_rendement:
            self.rendement_actuel = dernier_rendement.rendement_ha
            
            # Calculer l'évolution
            if self.rendement_precedent and self.rendement_precedent > 0:
                self.evolution_rendement = ((self.rendement_actuel - self.rendement_precedent) / self.rendement_precedent) * 100
        
        # Prédiction de rendement (simulation)
        if self.saison_courante in ['ete', 'automne']:
            self.rendement_predit = self.rendement_actuel * 1.1  # +10% pour la saison
            self.confiance_prediction = 85.0
        else:
            self.rendement_predit = self.rendement_actuel * 0.9  # -10% pour l'hiver
            self.confiance_prediction = 75.0
    
    def _mettre_a_jour_interventions(self):
        """Met à jour les informations d'intervention"""
        # Compter les interventions planifiées
        interventions_planifiees = self.env['intervention.agri'].search([
            ('parcelle_id.exploitation_id', '=', self.exploitation_id.id),
            ('date_planifiee', '>=', datetime.now()),
            ('statut', '=', 'planifiee')
        ])
        
        self.interventions_planifiees = len(interventions_planifiees)
        
        # Calculer le coût total
        self.cout_interventions = sum(intervention.cout_estime for intervention in interventions_planifiees)
        
        # Compter les interventions réalisées
        interventions_realisees = self.env['intervention.agri'].search([
            ('parcelle_id.exploitation_id', '=', self.exploitation_id.id),
            ('statut', '=', 'terminee')
        ])
        
        self.interventions_realisees = len(interventions_realisees)
        
        # Calculer l'efficacité (simulation)
        if self.interventions_realisees > 0:
            self.efficacite_interventions = 85.0  # Simulation
            self.retour_investissement = 120.0  # Simulation
    
    def _mettre_a_jour_ressources(self):
        """Met à jour les informations de ressources"""
        # Calculer la consommation d'eau (simulation)
        self.consommation_eau = self.superficie_totale * 500  # 500 m³/ha
        self.disponibilite_eau = self.superficie_totale * 800  # 800 m³/ha
        
        if self.disponibilite_eau > 0:
            self.efficacite_irrigation = (self.consommation_eau / self.disponibilite_eau) * 100
        
        # Calculer le stress hydrique
        if self.disponibilite_eau > 0:
            ratio = self.consommation_eau / self.disponibilite_eau
            self.stress_hydrique = min(1.0, max(0.0, ratio - 0.5))
        
        # Nutriments du sol (simulation)
        self.azote_sol = 120.0
        self.phosphore_sol = 80.0
        self.potassium_sol = 150.0
        self.ph_sol = 6.8
        
        # Énergie (simulation)
        self.consommation_energie = self.superficie_totale * 250  # 250 kWh/ha
        self.efficacite_energetique = 75.0
        
        # Main d'œuvre (simulation)
        self.heures_travail = self.superficie_totale * 15  # 15 h/ha
        self.productivite_travail = 25.0  # 25 €/h
        self.cout_main_oeuvre = self.heures_travail * self.productivite_travail
    
    def _mettre_a_jour_qualite(self):
        """Met à jour les informations de qualité"""
        # Indice de qualité (simulation basée sur les ressources)
        qualite_base = 70.0
        
        # Bonus pour bonne gestion
        if self.efficacite_irrigation > 80:
            qualite_base += 10
        if self.ph_sol >= 6.0 and self.ph_sol <= 7.5:
            qualite_base += 10
        if self.rotation_cultures:
            qualite_base += 5
        
        self.indice_qualite = min(100.0, qualite_base)
        
        # Conformité standards
        self.conformite_standards = self.indice_qualite * 0.9
        
        # Satisfaction clients (simulation)
        self.satisfaction_clients = self.indice_qualite * 0.95
    
    def _mettre_a_jour_durabilite(self):
        """Met à jour les informations de durabilité"""
        # Émissions CO2 (simulation)
        self.emissions_co2 = self.superficie_totale * 150  # 150 kg/ha
        
        # Utilisation pesticides (simulation)
        self.utilisation_pesticides = self.superficie_totale * 2.5  # 2.5 kg/ha
        
        # Biodiversité (simulation basée sur les pratiques)
        biodiversite_base = 60.0
        
        if self.agriculture_conservation:
            biodiversite_base += 15
        if self.rotation_cultures:
            biodiversite_base += 10
        if self.couverture_sol:
            biodiversite_base += 10
        if self.gestion_integree:
            biodiversite_base += 5
        
        self.biodiversite = min(100.0, biodiversite_base)
    
    def calculer_kpis(self):
        """Calcule les indicateurs clés de performance"""
        self.ensure_one()
        
        kpis = {
            'rendement': {
                'actuel': self.rendement_actuel,
                'evolution': self.evolution_rendement,
                'objectif': self.objectif_rendement
            },
            'ressources': {
                'efficacite_eau': self.efficacite_irrigation,
                'efficacite_energie': self.efficacite_energetique,
                'stress_hydrique': self.stress_hydrique
            },
            'qualite': {
                'indice': self.indice_qualite,
                'conformite': self.conformite_standards,
                'satisfaction': self.satisfaction_clients
            },
            'durabilite': {
                'biodiversite': self.biodiversite,
                'emissions_co2': self.emissions_co2,
                'pesticides': self.utilisation_pesticides
            }
        }
        
        return kpis
    
    def generer_rapport_agricole(self):
        """Génère un rapport agricole complet"""
        self.ensure_one()
        
        # Calculer tous les KPIs
        kpis = self.calculer_kpis()
        
        # Créer le rapport
        rapport = {
            'exploitation': self.exploitation_id.name,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'kpis': kpis,
            'recommandations': self._generer_recommandations(kpis)
        }
        
        return rapport
    
    def _generer_recommandations(self, kpis):
        """Génère des recommandations basées sur les KPIs"""
        recommandations = []
        
        # Recommandations rendement
        if kpis['rendement']['evolution'] < -5:
            recommandations.append("Analyser les causes de baisse de rendement et ajuster les pratiques culturales")
        
        # Recommandations ressources
        if kpis['ressources']['efficacite_eau'] < 70:
            recommandations.append("Optimiser l'irrigation et vérifier l'état du système")
        
        if kpis['ressources']['stress_hydrique'] > 0.7:
            recommandations.append("Intervention urgente requise pour l'irrigation")
        
        # Recommandations qualité
        if kpis['qualite']['indice'] < 75:
            recommandations.append("Améliorer la gestion des ressources et des pratiques culturales")
        
        # Recommandations durabilité
        if kpis['durabilite']['biodiversite'] < 70:
            recommandations.append("Renforcer les pratiques favorables à la biodiversité")
        
        if kpis['durabilite']['emissions_co2'] > 200:
            recommandations.append("Optimiser l'utilisation des machines et des intrants")
        
        return recommandations
