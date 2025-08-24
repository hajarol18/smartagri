from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Intrant(models.Model):
    _name = "intrant.agri"
    _inherits = {"product.template": "product_tmpl_id"}

    product_tmpl_id = fields.Many2one(
        "product.template", required=True, ondelete="cascade"
    )
    exploitation_id = fields.Many2one("exploitation.agri", string="Exploitation")
    stock_minimum = fields.Float(string="Stock minimum")
    type_intrant = fields.Selection([
        ('semence', 'Semences'),
        ('engrais', 'Engrais'),
        ('pesticide', 'Pesticides'),
        ('irrigation', 'Eau d\'irrigation'),
        ('autre', 'Autre')
    ], string='Type d\'intrant')

    @api.model
    def get_stock_alert(self):
        """Retourne les intrants avec un stock faible"""
        return self.filtered(lambda r: 0 < r.qty_available <= r.stock_minimum) 