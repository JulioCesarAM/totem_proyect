# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Event(models.Model):
    _name = 'event.totem'
    name = fields.Text(string=_(''))
    title = fields.Text(string=_(''))
    bannerImg = fields.Binary(string=_(''))
    sliderImg = fields.One2many('slider.totem', 'event_id_fk', string=_(''))
    description = fields.Text(string=_(''))
    footer = fields.Text(string=_(''))
    qr = fields.Text()
    #sliderImgTimer = fields.Integer(string='')
    sliderImgTimer = fields.Float(compute='_compute_sliderImgTimer', string='')
    
    @api.depends('')
    def _compute_sliderImgTimer(self):
        self.sliderImgTimer=self.env['ir.config_parameter'].sudo().get_param('totem_proyect.totem_proyect_img_slider_control')
        pass



