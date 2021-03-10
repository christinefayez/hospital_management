from datetime import date
from odoo import models, fields, api
from odoo.exceptions import UserError
import re


class HmsPatient(models.Model):
    _name = "hms.patient"
    _rec_name = "first_name"
    _description = "Patient Model"
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    history = fields.Html('Patient History')
    cr_ratio = fields.Float(default=False)
    blood_type = fields.Selection([
        ('o-', 'O-'),
        ('o+', 'O+'),
        ('a-', 'A-'),
        ('a+', 'A+'),
        ('b-', 'B-'),
        ('b+', 'B+'),
        ('ab-', 'AB-'),
        ('ab+', 'AB+'),
    ])
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer(compute="_calc_age")
    status = fields.Selection([
        ('u', 'Undetermined'),
        ('g', 'Good'),
        ('f', 'Fair'),
        ('s', 'Serious'),
    ], string="Select status", default='u')
    department_id = fields.Many2one('hms.department')
    department_capacity = fields.Integer(related="department_id.capacity")
    doctor_ids = fields.Many2many("hms.doctor")
    history_ids = fields.One2many('hms.patient.history', 'patient_id')
    email = fields.Char()

    _sql_constraints = [
        ('email_unique_field', "UNIQUE(email)", 'Email Already Exists')
    ]

    @api.depends('birth_date')
    def _calc_age(self):
        for rec in self:
            if rec.birth_date:
                rec.age = date.today().year - rec.birth_date.year
            else:
                rec.age = 0

    @api.constrains('email')
    def _check_email(self):
        if self.email and not re.search('^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{3,}$', self.email):
            raise UserError("Not valid Email")

    @api.onchange("age")
    def _on_age_change(self):
        if self.age and (self.age > 0) and self.age < 30:
            self.pcr = True

            return {
                'warning': {
                    'title': "Warning",
                    "message": "PCR checked ya prince"
                }
            }

    def change_status(self, new_status, new_status_string, patient):
        patient.status = new_status
        # store new record in the
        self.env["hms.patient.history"].create(
            {'description': f'State changed to {new_status_string}',
             'patient_id': patient.id})

    def set_patient_status_good(self):
        for patient in self:
            patient.change_status('g', 'good', patient)
            # patient.status = 'g'
            # store new record in the
            # self.env["hms.patient.history"].create(
            #     {'description': 'State changed to Good',
            #      'patient_id': patient.id})

    def set_patient_status_fair(self):
        for patient in self:
            patient.change_status('f', 'fair', patient)

    def set_patient_status_serious(self):
        for patient in self:
            patient.change_status('s', 'serious', patient)
