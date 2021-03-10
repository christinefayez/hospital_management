from odoo import models, fields


class HmsDoctor(models.Model):
    _name = "hms.doctor"

    _rec_name = "first_name"
    _description = "Doctor model"
    first_name = fields.Char()
    last_name = fields.Char()
    specialization = fields.Selection([
        ('a', 'Allergists'),
        ('b', 'Anesthesiologists'),
        ('c', 'Cardiologists'),
        ('d', 'Dermatologists'),
    ])
    image = fields.Binary()
    department_ids = fields.Many2many("hms.department")
