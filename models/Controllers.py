from odoo import models,fields,api,_,exceptions
import logging
class Controllers(models.Model):
    _name='totem.controllers'
    name = fields.Text(string='')
    admin = fields.Many2one('res.users', string=_(''))
    events = fields.Many2many('event.totem', string=_(''))

    