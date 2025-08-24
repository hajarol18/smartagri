from odoo import models, fields, api

class InterventionAgri(models.Model):
    _name = 'intervention.agri'
    _description = 'Intervention Agricole'
    _inherit = 'project.task'
    
    # Champs spécifiques aux interventions agricoles
    type_intervention = fields.Selection([
        ('semis', 'Semis'),
        ('recolte', 'Récolte'),
        ('traitement', 'Traitement'),
        ('irrigation', 'Irrigation'),
        ('fertilisation', 'Fertilisation'),
        ('autre', 'Autre')
    ], string='Type d\'intervention', required=True)
    
    cout_estime = fields.Float(string='Coût estimé (€)', default=0.0)
    duree_estimee = fields.Float(string='Durée estimée (heures)', default=1.0)
    
    # Relations agricoles
    exploitation_id = fields.Many2one('exploitation.agri', string='Exploitation')
    parcelle_id = fields.Many2one('parcelle.agri', string='Parcelle')
    culture_id = fields.Many2one('culture.agri', string='Culture')
    intrants_ids = fields.Many2many('intrant.agri', string='Intrants utilisés')
    
    # Surcharge du nom pour l'affichage
    name = fields.Char(string='Nom de l\'intervention', required=True, default='Nouvelle Intervention')
    
    @api.model
    def create(self, vals):
        # Créer d'abord la tâche
        task_vals = {
            'name': vals.get('name', 'Nouvelle Intervention'),
            'project_id': self.env.ref('project.project_default').id if self.env.ref('project.project_default', raise_if_not_found=False) else False,
        }
        task = self.env['project.task'].create(task_vals)
        vals['id'] = task.id
        return super().create(vals)
    
    # exemple d'action d'annulation
    def action_annuler(self):
        cancelled_stage = self.env.ref("project.project_stage_cancelled")
        for record in self:
            record.stage_id = cancelled_stage 