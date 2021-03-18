from odoo import models, fields, api

class image_slider(models.Model):
    _name = 'slider.totem'
    name = fields.Text(string='')
    image_rute = fields.Binary()
    event_id_fk = fields.Many2one(compute='generate_fk',comodel_name='event.totem', string='Anuncio')
    
    