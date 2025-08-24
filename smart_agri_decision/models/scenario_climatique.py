from odoo import models, fields, api

class ScenarioClimatique(models.Model):
    _name = "scenario.climatique"
    _description = "Scénario Climatique RCP"

    scenario_rcp = fields.Selection([
        ("rcp45", "RCP 4.5"),
        ("rcp85", "RCP 8.5"),
    ], required=True)
    annee = fields.Integer(required=True)
    temperature = fields.Float(string="Température moyenne (°C)")
    precipitation = fields.Float(string="Précipitations (mm)")
    impact_agricole = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé'),
        ('critique', 'Critique')
    ], string='Impact agricole', compute='_compute_impact_agricole', store=True)
    
    @api.depends('temperature', 'precipitation')
    def _compute_impact_agricole(self):
        """Calcule l'impact agricole basé sur température et précipitations"""
        for record in self:
            impact_score = 0
            
            # Impact température (seuil à 25°C)
            if record.temperature > 30:
                impact_score += 3
            elif record.temperature > 25:
                impact_score += 2
            elif record.temperature > 20:
                impact_score += 1
            
            # Impact précipitations (seuil à 400mm)
            if record.precipitation < 200:
                impact_score += 3
            elif record.precipitation < 300:
                impact_score += 2
            elif record.precipitation < 400:
                impact_score += 1
            
            # Classification de l'impact
            if impact_score >= 5:
                record.impact_agricole = 'critique'
            elif impact_score >= 3:
                record.impact_agricole = 'eleve'
            elif impact_score >= 1:
                record.impact_agricole = 'modere'
            else:
                record.impact_agricole = 'faible'
