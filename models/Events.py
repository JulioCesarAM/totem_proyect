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
    #RSS video
    #RSS datos
    def write(self, vals):
        #records = self.env['event.totem'].write({
         #   'description' : 'holita'

        #})
        #_logger.info("500 self = :" + str(self.description))
        _logger.info("%s 500",vals)
    
        #self.write({
        #    'description' : 'hola'
        #})
      
        if vals['bannerPrincipalSelector']=='img':
            vals['description']="imagen"
        else
            vals['description']="nada"

        record = super(Event,self).write(vals)
        _logger.info("500 " + str(vals))
        #_logger.info("%s 500",record)
        #return record
        # va 
        return record

        #if record['bannerPrincipalSelector']=='img':
            #record['videoField']=False
            #record['urlVid']=False
        #elif record['bannerPrincipalSelector']=="vid":
            #record['bannerImg']=False
            #record['urlVid']=False
        #elif record['bannerPrincipalSelector']=="lvid":
            #record['bannerImg']=False
            #record['videoField']=False
        #print("entro")


  

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

