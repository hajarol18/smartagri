from odoo import models, fields

class Intervention(models.Model):
    _name = "intervention.agri"
    _inherit = "project.task"

    parcelle_id = fields.Many2one("parcelle.agri", string="Parcelle")
    culture_id = fields.Many2one("culture.agri", string="Culture")
    intrants_ids = fields.One2many(
        "intrant.agri", "intervention_id", string="Intrants utilisés"
    )
    type_intervention = fields.Selection([
        ('semis', 'Semis'),
        ('irrigation', 'Irrigation'),
        ('fertilisation', 'Fertilisation'),
        ('traitement', 'Traitement phytosanitaire'),
        ('recolte', 'Récolte'),
        ('autre', 'Autre')
    ], string='Type d\'intervention')
    cout_estime = fields.Float(string='Coût estimé (€)')
    duree_estimee = fields.Float(string='Durée estimée (heures)')

    # exemple d'action d'annulation
    def action_annuler(self):
        cancelled_stage = self.env.ref("project.project_stage_cancelled")
        for record in self:
            record.stage_id = cancelled_stage 