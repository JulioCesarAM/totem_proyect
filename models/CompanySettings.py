from odoo import fields,models,_,api,exceptions
class mainConfigValues(models.Model):
    _inherit='res.company'
    mainSlider = fields.Float(store="true")
    secundarySlider = fields.Float(store="true")
    description = fields.Text(store="true")
    companyQr = fields.Text(store="true")
    




   