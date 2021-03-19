# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Event(models.Model):
     _name = 'event.totem'
     name = fields.Text(sstring=_(''))
     title = fields.Text(string=_(''))
     bannerImg = fields.Binary(string=_(''))
     sliderImg = fields.One2many('slider.totem', 'event_id_fk', string=_(''))
     description = fields.Text(string=_(''))
     footer = fields.Text(string=_(''))
     qr = fields.Text()
    

