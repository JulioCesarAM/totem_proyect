from odoo import models, fields, api

class image_slider(models.Model):
    _name = 'image_slider.totem'
    image_id = fields.Integer()
    image_rute = fields.Binary(string='')
    image_event_id = fields.Integer(string='')