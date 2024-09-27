from odoo import fields, models

class estatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate property Type"
    name = fields.Char(required=True)
    _sql_constraints = [
        ('unique_property_type_name', 'unique(name)', 'The property type name must be unique!'),
    ]