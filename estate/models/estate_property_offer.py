from odoo import fields, models

class estatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Estate Property Offer"
    price = fields.Float()
    status = fields.Selection(
        selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')],
        copy = False
    )
    partner_id = fields.Many2one("res.partner", required = True)
    property_id = fields.Many2one("estate_property",required = True)
