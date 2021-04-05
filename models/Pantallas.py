from odoo import models,fields,api,_,exceptions
import logging
class Pantallas(models.Model):
    _name = 'pantallas.totem'
    name = fields.Text(string='')
    userController = fields.Many2one('res.users', string='')
    eventsList = fields.Many2many('event.totem', string='')
    