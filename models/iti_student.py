from odoo import models, fields, api
from odoo.exceptions import UserError


class itiStudent(models.Model):
    _name = "iti.student"

    name = fields.Char()
    email = fields.Char()
    salary = fields.Float()
    tax = fields.Float(compute="check_salary")
    salary_net = fields.Float(compute="check_salary")
    birthday = fields.Date()
    address = fields.Text()
    gender = fields.Selection(
        [('M', 'Male'), ('F', 'Female')]
    )
    details = fields.Html()
    track_id = fields.Many2one("iti.track")
    skill_id = fields.Many2many("iti.skill")
    track_capacity = fields.Integer(related="track_id.cap")
    state = fields.Selection(
        [
            ("applied", "Applied"),
            ("first", "First Interview"),
            ("second", "Second Interview"),
            ("passed", "Passed"),
            ("rejected", "rejected"),

        ], default='applied'
    )

    @api.constrains
    def check_salary2(self):
        for rec in self:
            if rec.salary > 10000:
                raise UserError("salary greater than 10000")

    @api.depends("salary")
    def check_salary(self):
        for rec in self:
            rec.tax = rec.salary * .20
            rec.salary_net = rec.salary - rec.tax

    @api.model
    def create(self, vals_list):
        print("vals in create ", vals_list)
        name_split = vals_list['name'].split()
        vals_list['email'] = f"{name_split[0]}.{name_split[1]}@gmail.com"
        student_search = self.search([("email", "=", vals_list['email'])])
        if student_search:
            raise UserError('email already exist')
        return super().create(vals_list)

    def write(self, vals_list):
        for rec in self:
            print("object ", self)
            print("name ", self.name)
            print("vals list ", vals_list)
            if vals_list.get("name", False):
                name_split = vals_list['name'].split()
                vals_list['email'] = f"{name_split[0]}.{name_split[1]}@gmail.com"
        super().write(vals_list)
        print("object ", self)
        print("name ", self.name)

    def unlink(self):
        for rec in self:
            # object.mapped('field_name')
            print("rec state ", rec.state)
            print("rec state ", rec.mapped('state'))
            if rec.state in ['passed', 'rejected']:
                raise UserError("You Can't Delete Passed/Rejected Students")
        super().unlink()

    def on_change(self):
        if self.state == 'applied':
            self.state = 'first'
        elif self.state == 'first':
            self.state = 'second'

        elif self.state in ["passed", "rejected", "first", "second"]:
            self.state = 'applied'

    def set_passed(self):
        self.state = 'passed'

    def set_applied(self):
        self.write({"state": "applied"})

    def set_first(self):
        self.state = 'first'

    def set_second(self):
        self.state = 'second'

    def set_rejected(self):
        self.state = 'rejected'

    @api.onchange("gender")
    # change name value base on gender value .
    def _on_change_gender(self):
        self.name = " "
        if self.gender == "M":
            self.name = "Ahmed"
        else:
            self.name = "Asmaa"
        return {
            "warning": {
                "title": "Warning",
                "message": " you are changing gender value "
            }
        }
