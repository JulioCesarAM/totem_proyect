from odoo import models,fields,api,_,exceptions
import logging
class Controllers(models.Model):
    _name='totem.controllers'
    name = fields.Text(string='')
    admin = fields.Many2one('res.users', string=_(''))
    events = fields.Many2many('event.event', string=_(''))
    #access_events_totem,totem_proyect,model_event_totem,,1,1,1,1

    