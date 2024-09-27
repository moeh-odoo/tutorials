from odoo import fields, models

class estatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "Estate property Tag"
    name = fields.Char(required=True)
    _sql_constraints = [
        ('unique_property_tag_name', 'unique(name)', 'The tag name must be unique, regardless of case!'),
    ]

