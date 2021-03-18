# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Event(models.Model):
     _name = 'event.totem'
     event_id = fields.Integer(string='')
     event_name = fields.Text(string='')
     event_banner_img = fields.Binary(string='')
     event_slider_img = fields.Many2one('comodel_name', string='')
     event_description = fields.Text(string='')
     event_qr = fields.Text(string='')
    

