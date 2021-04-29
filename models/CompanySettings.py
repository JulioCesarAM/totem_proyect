from odoo import fields,models,_,api,exceptions, tools
from odoo.modules.module import get_module_resource
import base64
class mainConfigValues(models.Model):
    _inherit='res.company'
    mainSlider = fields.Float()
    secundarySlider = fields.Float()
    description = fields.Text()
    companyQr = fields.Text()
    refreshTime = fields.Integer(string=_(''))
    redirectionTime = fields.Integer(string=_(''))
    backGroundImg = fields.Binary(string=_(''))
    lostConnectionImg = fields.Binary(string=_(''))
    colorBar = fields.Text()
    colorLines = fields.Text()
