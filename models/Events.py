# -*- coding: utf-8 -*-

from odoo import models, fields, api, _,exceptions


class Event(models.Model):
    _name = 'event.totem'
    title = fields.Text(string=_(''))
    bannerImg = fields.Binary(string=_(''))
    sliderImg = fields.One2many('slider.totem', 'event_id_fk', string=_(''))
    description = fields.Text(string=_(''))
    qr = fields.Text()
    bannerPrincipalSelector = fields.Selection([
        ('imagen', 'img'),
        ('video', 'vid')
        #('rss_video', 'rssv'),
        #('rss_datos', 'rssd'),
    ], string=_(''))
    audioField = fields.Binary(string='')
    videoField = fields.Binary(string='')
    #RSS video
    #RSS datos
    @api.multi
    def write(self, vals):
        if self.bannerPrincipalSelector=='img':
            self.videoField = False
        elif self.bannerPrincipalSelector=="vid":
            self.bannerImg = False
         
        return super().write(vals)
  

    @api.constrains('description')
    def _constrains_description(self):
        if len(self.description) > 461:
            raise exceptions.ValidationError(_("limite de caracteres 461")) 
        pass
    @api.constrains('title')
    def _constrains_title(self):
        if len(self.title) > 41:
            raise exceptions.ValidationError(_("limite de caracteres 41")) 
        pass

