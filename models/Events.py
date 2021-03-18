# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Event(models.Model):
     _name = 'event.totem'
     name = fields.Text(string='')
     title = fields.Text(string='')
     bannerImg = fields.Binary(string='')
     sliderImg = fields.One2many('slider.totem', 'event_id_fk', string='')
     description = fields.Text(string='')
     footer = fields.Text(string='')
     qr = fields.Text()
    

