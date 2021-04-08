# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions
import logging
import re
from datetime import *

_logger = logging.getLogger(__name__)


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
        ('lvid', 'Url video')
        #('rss_video', 'rssv'),
        #('rss_datos', 'rssd'),
    ], string=_(''), default='img')
    audioField = fields.Binary(string=_(''))
    videoField = fields.Binary(string=_(''))
    urlVid = fields.Text(string=_(''))
    horaInicio = fields.Float(string=_(''))
    horaFin = fields.Float(string=_(''))
    urlWeb = fields.Text(string=_(''))
    fechaInicio = fields.Date(string=_(''))
    fechaFin = fields.Date(string=_(''))
    # RSS video
    # RSS datos
    urlVidId = fields.Text(string=_(''))
    logo = fields.Binary(string=_(''))
    descriptionPopUp = fields.Text(string=_(''))
    titlePopUp = fields.Text(string=_(''))
    popUpImg = fields.Binary(string='')
    #metodo diseñado para devolver todos los eventos que peternecen al usuario que los controla
    @api.model
    def get_events(self, uid):
        
        events_ids = self.env['totem.controllers'].search_read([('admin','=',uid)])
        events = self.env['event.totem'].search_read([('id','in',events_ids[0]['events'])],[
            'title','sliderImg','description','qr',
            'bannerPrincipalSelector','urlVid','horaInicio'
            ,'horaFin','fechaInicio','fechaFin','urlWeb'
            ,'urlVidId','descriptionPopUp','titlePopUp'])
        #events[0]['title']=self.timeToMiliCovnerter(events[0]['fechaInicio'])

    
      




        _logger.info(str(events[0]['fechaInicio'])+" 500")
        #aux = self.env['event.totem'].search_read(['id','in',auxId])
        #2021 |- 04 | - 06
        return events
    
    #def timeToMiliCovnerter(self,date):
       # dayString=date.rsplit('-',1)[0]
       # dayInteger=int(dayString)
        #dayInteger+=self.leapYear(dayInteger)
    
        #aux=date.fromisoformat(str(date))
        #return aux.timestamp()*1000
       # pass

    #def leapYear(self,date):
     #   FINAL_DATE=1972
      #  return int(((date-FINAL_DATE)/4)+1)
       # pass

    @api.onchange('urlVid', 'urlVidId')
    def _onchange_(self):
        if self.urlVid is not False:
            if not re.search('/embed/', self.urlVid):
                self.urlVid = self.urlVid[:24] + 'embed/' + self.urlVid[24:]
            if re.search('/watch\?v\=', self.urlVid):
                self.urlVid = self.urlVid.replace("/watch?v=", "/")
            self.urlVidId = self.urlVid[30:]
        pass

    @api.onchange('qr')
    def _onchange_qr(self):
        if self.urlWeb is False:
            self.urlWeb = self.qr
        pass

    @api.multi
    def write(self, vals):
        if 'bannerPrincipalSelector' in vals.keys():
            if vals['bannerPrincipalSelector'] == 'img':
                vals['videoField'] = False
                vals['urlVid'] = False
            elif vals['bannerPrincipalSelector'] == "vid":
                vals['bannerImg'] = False
                vals['urlVid'] = False
            elif vals['bannerPrincipalSelector'] == "lvid":
                vals['bannerImg'] = False
                vals['videoField'] = False

        # if 'qr' in vals.keys() and 'urlWeb' not in vals.keys():
        #    vals['urlWeb'] = vals['qr']

        return super(Event, self).write(vals)

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
