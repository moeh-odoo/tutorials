from odoo import api, fields, models
from odoo.exceptions import UserError

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
    offer_ids = fields.One2many("estate_property_offer","property_id",string="offer") # [21,23,24].mapped
    total_area = fields.Float(compute="_compute_total")
    state = fields.Selection(
        selection=[('new', 'New'), 
                ('received', 'Received'), 
                ('accepted', 'Accepted'), 
                ('sold', 'Sold'), 
                ('canceled', 'Canceled')],
        required=True,
        default='new',
        string="Status"
    )

    @api.depends("garden_area","living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area;

    best_price = fields.Float(compute="_compute_best_price")

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            print(record)
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden: 
            self.garden_area =10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    garden_orientation = fields.Selection(
        selection=[('North', 'north'), ('South', 'south'), ('East','east'), ('West','west')]
    )

    def action_set_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled properties cannot be marked as sold.")
            record.state = 'sold'
        return True

    def action_set_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            record.state = 'canceled'
        return True