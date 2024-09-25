from odoo import fields, models

class estatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate property Type"
    name = fields.Char(required=True)