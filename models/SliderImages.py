from odoo import models, fields, api, _

class image_slider(models.Model):
    _name = 'slider.totem'
    name = fields.Text(string=_(''))
    image_rute = fields.Binary()
    event_id_fk = fields.Many2one(comodel_name='event.totem', string=_('Anuncio'))