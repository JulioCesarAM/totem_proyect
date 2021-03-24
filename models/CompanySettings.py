from odoo import fields,models,_,api,exceptions
class mainConfigValues(models.Model):
    _inherit='res.company'
    mainSlider = fields.Float()
    secundarySlider = fields.Float()
    description = fields.Text()
    companyQr = fields.Text()
    prueba = fields.Integer(string='')




   