from odoo import models, fields


class itiTrack(models.Model):
    _name = "iti.track"
    name = fields.Char()
    cap = fields.Integer()
    is_open = fields.Boolean()
    student_id = fields.One2many("iti.student", "track_id")
