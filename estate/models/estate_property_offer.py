from odoo import api, fields, models
from datetime import date
from odoo.exceptions import UserError,ValidationError

class estatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Estate Property Offer"
    price = fields.Float()
    status = fields.Selection(
        selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')],
        copy = False
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute = "_compute_date_deadline", inverse = "_inverse_date_deadline")
    partner_id = fields.Many2one("res.partner", required = True)
    property_id = fields.Many2one("estate_property",required = True)

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'The offer price must be strictly positive')
    ]
    #fields.Date.add(fields.Date.today(), months=3)
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                # Calculate the difference between date_deadline and today's date
                today = fields.Date.today()  # Get today's date
                deadline = fields.Date.from_string(record.date_deadline)  # Convert deadline to date object
                days_difference = (deadline - date.today()).days  # Subtract today's date from deadline
                
                # Assign the difference in days to the 'validity' field
                record.validity = days_difference

    def action_to_accept(self):
        for record in self:
            if record.price*100 < record.property_id.expected_price*90:
                raise ValidationError("The selling price must be at least 90% of the expected price.")
            else:
                record.status = "Accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id

    def action_to_refuse(self):
        for record in self:
            record.status = "Refused"
