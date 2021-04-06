from odoo import models,fields,api,_,exceptions
import logging
class Users(models.Model):
    _inherit='res.users'
    pantallas = fields.One2many('pantallas.totem', 'userController', string='')
    @api.model
    def create(self, vals):
        return super(Users,self).create(vals)
    