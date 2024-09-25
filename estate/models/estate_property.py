from odoo import fields, models

class estateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate property table to store the data"

    name = fields.Char(required=True)
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    Active = fields.Boolean(default=True)
    estate_property_type_id = fields.Many2one("estate_property_type",string = "property type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    sales_person_id = fields.Many2one("res.users", string="Sales")
    estate_property_tag_id = fields.Many2many("estate_property_tag", string="Property Tags")
    offer_ids = fields.One2many("estate_property_offer","property_id",string="offer")
    garden_orientation = fields.Selection(
        selection=[('North', 'north'), ('South', 'south'), ('East','east'), ('West','west')]
    )
    state = fields.Selection(
        selection = [('New',''), ('Received',''), ('Accepted',''), ('Sold',''), ('Canceled','')],
        required = True,
        copy = False,
        default = 'New'
    )