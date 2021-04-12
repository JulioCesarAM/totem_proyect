# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions
import logging
import re
from datetime import *
from urllib.request import urlopen
from xml.etree.ElementTree import *

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
        ('vid', 'Subir video'),# eliminar lvid
        ('lvid', 'Url video'),
        ('rssVideo', 'rssv') #renombrar eso
        #('rss_datos', 'rssd'),
    ], string=_(''), default='img')
    audioField = fields.Binary(string=_(''))
    videoField = fields.Binary(string=_(''))
    urlVid = fields.Text(string=_(''))
    horaInicio = fields.Float(string=_(''),digits=(12,2))
    horaFin = fields.Float(string=_(''),digits=(12,2))
    urlWeb = fields.Text(string=_(''))
    fechaInicio = fields.Date(string=_(''))
    fechaFin = fields.Date(string=_(''))
    rssVideo = fields.Text(string=_(''))
    # RSS datos
    urlVidId = fields.Text(string=_(''))
    logo = fields.Binary(string=_(''))
    descriptionPopUp = fields.Text(string=_(''))
    titlePopUp = fields.Text(string=_(''))
    popUpImg = fields.Binary(string=_(''))
    #metodo diseñado para devolver todos los eventos que peternecen al usuario que los controla
    @api.model
    def get_events(self, uid):
        
        events_ids = self.env['totem.controllers'].search_read([('admin','=',uid)])
        events = self.env['event.totem'].search_read([('id','in',events_ids[0]['events'])],[
            'title','sliderImg','description','qr',
            'bannerPrincipalSelector','urlVid','horaInicio'
            ,'horaFin','fechaInicio','fechaFin','urlWeb'
            ,'urlVidId','descriptionPopUp','titlePopUp','rssVideo'])


        #upgrades
            #implementar que se envie el enlace completo del video modo url vid
            #eliminar valores que no son necesarios del campo events
            #generar varios events dependiendo del modo selecionado

        for i in events:
            if i['bannerPrincipalSelector']=='rssVideo':
                i['rssVideo']=self.getXmlData(i['rssVideo'])
            
            i['horaInicio']=self.hourConverterToSeconds(i['horaInicio'])
            i['horaFin']=self.hourConverterToSeconds(i['horaFin'])

        return events
    
    def hourConverterToSeconds(self,time):
        timeHour=str(time).rsplit('.',1)[0]
        timeMin=str(time).rsplit('.',1)[1]
        if len(timeMin)<=1:
            timeMin=str(timeMin)+"0"
        minToMilSec=int(timeMin)*60*1000
        hourToMilSec=int(timeHour)*60*60*1000
 
        return hourToMilSec+minToMilSec
        pass

    def getXmlData(self,url):
        getXmlFromUrl=urlopen(url)
        dataFromXml=parse(getXmlFromUrl)
        return self.processXml(dataFromXml)
        pass
    def processXml(self,xml):
        container=[]
        enlaceCompleto="https://www.youtube.com/embed/"
        root=xml.getroot()
        for entry in root:
            if entry.tag.rsplit('}',1)[1]=='entry':
                for media in entry:
                    if media.tag.rsplit('}',1)[1]=='group':
                        for content in media:
                            if content.tag.rsplit('}',1)[1]=='content':
                                container.append(self.filter(content.attrib['url']))
                                #_logger.info(str(content.attrib['url'])+" 500")
                                #posible implementacion de expresiones regulares stby
        
        enlaceCompleto += container[0] + "?autoplay=1&mute=1&controls=0&rel=0&loop=1&playlist="

        #mejorar
        for urlId in container:
            enlaceCompleto+=urlId+","
        return enlaceCompleto

        #_logger.info(str(enlaceCompleto)+ " 500")
        pass

    def filter(self,url):
        #_logger.info(str(url.rsplit('/v/',1)[1].rsplit('?',1)[0])+" 500")
        return url.rsplit('/v/',1)[1].rsplit('?',1)[0]
        pass
    
    #extrar filtro
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
    #adaptar a los cambios implementados en el banner selector
     #lvid eliminado y reemplazado por el rss

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
