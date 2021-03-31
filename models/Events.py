# -*- coding: utf-8 -*-

from odoo import models, fields, api, _,exceptions
import logging

_logger=logging.getLogger(__name__)
class Event(models.Model):
    _name = 'event.totem'
    title = fields.Text(string=_(''))
    bannerImg = fields.Binary(string=_(''))
    sliderImg = fields.One2many('slider.totem', 'event_id_fk', string=_(''))
    description = fields.Text(string=_(''))
    qr = fields.Text()
    bannerPrincipalSelector = fields.Selection([
        ('img', 'Imagen'),
        ('vid', 'Subir video'),
        ('lvid','Url video')
        #('rss_video', 'rssv'),
        #('rss_datos', 'rssd'),
    ], string=_(''),default='img')
    audioField = fields.Binary(string=_(''))
    videoField = fields.Binary(string=_(''))
    urlVid = fields.Text(string=_(''))
    fechaInicio = fields.Datetime(string=_(''))
    fechaFin = fields.Datetime(string=_(''))
    #RSS video
    #RSS datos

    @api.multi
    def write(self, vals):
        if 'bannerPrincipalSelector' in vals.keys():
            if vals['bannerPrincipalSelector']=='img':
                vals['videoField']=False
                vals['urlVid']=False
            elif vals['bannerPrincipalSelector']=="vid":
                vals['bannerImg']=False
                vals['urlVid']=False
            elif vals['bannerPrincipalSelector']=="lvid":
                vals['bannerImg']=False
                vals['videoField']=False
        return super(Event,self).write(vals)

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

