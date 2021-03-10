from odoo import models, fields


class HmsPatientHistory(models.Model):
    _name = "hms.patient.history"
    _description = "Patient History Model"
    description = fields.Text()
    patient_id = fields.Many2one('hms.patient')
