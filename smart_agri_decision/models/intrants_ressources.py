from odoo import models, fields, api

class IntrantAgri(models.Model):
    _name = 'intrant.agri'
    _description = 'Intrant Agricole'
    _inherits = {'product.template': 'product_tmpl_id'}

    product_tmpl_id = fields.Many2one('product.template', string='Produit', required=True, ondelete='cascade')
    
    # Champs spécifiques aux intrants agricoles
    type_intrant = fields.Selection([
        ('engrais', 'Engrais'),
        ('pesticide', 'Pesticide'),
        ('semence', 'Semence'),
        ('materiel', 'Matériel'),
        ('autre', 'Autre')
    ], string='Type d\'intrant', required=True)
    
    stock_minimum = fields.Float(string='Stock minimum', default=0.0)
    stock_disponible = fields.Float(string='Stock disponible', compute='_compute_stock_disponible', store=True)
    
    # Relations
    exploitation_id = fields.Many2one('exploitation.agri', string='Exploitation')
    fournisseur_id = fields.Many2one('res.partner', string='Fournisseur')
    
    @api.depends('qty_available')
    def _compute_stock_disponible(self):
        for record in self:
            record.stock_disponible = record.qty_available or 0.0
    
    @api.model
    def create(self, vals):
        # Créer d'abord le produit
        product_vals = {
            'name': vals.get('name', 'Nouvel Intrant'),
            'type': 'product',  # Stockable
            'categ_id': self.env.ref('product.product_category_all').id,
            'list_price': vals.get('list_price', 0.0),
            'standard_price': vals.get('standard_price', 0.0),
        }
        product = self.env['product.template'].create(product_vals)
        vals['product_tmpl_id'] = product.id
        return super().create(vals)
    
    def get_stock_alert(self):
        """Retourner les intrants avec stock faible"""
        return self.filtered(lambda r: 0 < r.stock_disponible <= r.stock_minimum) 