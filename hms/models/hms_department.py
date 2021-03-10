from odoo import models, fields


class HmsDepartment(models.Model):
    _name = "hms.department"
    _description = "Department Model"

    name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()

    doctor_ids = fields.Many2many("hms.doctor")
