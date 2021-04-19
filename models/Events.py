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
    _order='sequence'
    name = fields.Char(string='')
    sequence = fields.Integer(string='')
    title = fields.Text(string=_(''))
    bannerImg = fields.Binary(string=_(''))
    sliderImg = fields.One2many('slider.totem', 'event_id_fk', string=_(''),ondelete='cascade')
    description = fields.Text(string=_(''))
    qr = fields.Text()
    bannerPrincipalSelector = fields.Selection([
        ('img', 'Imagen'),
        #('vid', 'Subir video'),# eliminar lvid
        ('lvid', 'Url video'),
        ('rssVideo', 'RSS video') #renombrar eso
        #('rss_datos', 'rssd'),
    ], string=_(''), default='img')
    audioField = fields.Binary(string=_(''))
    videoField = fields.Binary(string=_(''))
    urlVid = fields.Text(string=_(''))
    urlWeb = fields.Text(string=_(''))
 
    rssVideo = fields.Text(string=_(''))
  
    urlVidId = fields.Text(string=_(''))
    logo = fields.Binary(string=_(''))
    descriptionPopUp = fields.Text(string=_(''))
    titlePopUp = fields.Text(string=_(''))
    popUpImg = fields.Binary(string=_(''))
    fechas = fields.One2many('event.date', 'events', string=_(''))
    #metodo diseñado para devolver todos los eventos que peternecen al usuario que los controla
    @api.model
    def get_events(self, uid):
        events_ids = self.env['totem.controllers'].search_read([('admin','=',uid)])
        events = []
        
        if len(events_ids)>0:
            events = self.env['event.totem'].search_read([('id','in',events_ids[0]['events'])],[
                'title','sliderImg','description','qr','bannerImg',
                'bannerPrincipalSelector','urlVid','fechas','urlWeb'
                ,'urlVidId','descriptionPopUp','titlePopUp','rssVideo'])
            for i in events:
                if i['bannerPrincipalSelector']=='rssVideo':
                    i['rssVideo']=self.getXmlData(i['rssVideo'])
                if i['bannerPrincipalSelector']=='lvid':
                    i['urlVid']=self.urlVidProcessor(i['urlVid'])
                if i['fechas']!='':
                    i['fechas']=self.dateTimeProccessor(i['fechas'])
                    _logger.info(str(i['fechas'])+ " 500")
                    
        imgId=self.sliderImg
        dateId=self.fechas
        _logger.info(str(imgId)+ " 500")
        _logger.info(str(dateId)+ " 500")
    
        return events
        pass


    def dateTimeProccessor(self,date):
        fechas=self.env['event.date'].search_read([('id','in',date)],['fecha','rangoHoras','fechaFinal'])
        for fecha in fechas:
            timeInDate=self.env['event.time'].search_read([('id','in',fecha['rangoHoras'])],['horaInicial','horaFinal'])
            for time in timeInDate:
                time['horaInicial']=self.hourConverterToSeconds(time['horaInicial'])
                time['horaFinal']=self.hourConverterToSeconds(time['horaFinal'])
                fecha['rangoHoras'][timeInDate.index(time)]=time
        _logger.info(str(fechas) + " 500")

        return  fechas
        pass

    @api.multi
    def unlink(self):
        #self.env['slider.totem'].unlink([('id','in',imgId)])
        #self.env['event.date'].unlink([('id','in',dateId)])
        return super().unlink()


        
    def urlVidProcessor(self,url):
        idFromVid=url.rsplit('/embed/',1)[1]
        return url + "?autoplay=1&mute=1&controls=0&rel=0&loop=1&playlist="+idFromVid
        pass
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
    
    @api.model
    def create(self,vals):
        vals['name']=vals['title']
        record = super(Event,self).create(vals)
        _logger.info(str(vals['title'])+" 500")
        return record
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
 

    @api.multi
    def write(self, vals):
        try:
            _logger.info(str(vals['title'])+" 500")
            _logger.info(str(self['title'])+" 500")
            if vals['title']!='':
                vals['name']=vals['title']
            else:
                vals['name']=self['title']

            if 'bannerPrincipalSelector' in vals.keys():
                if vals['bannerPrincipalSelector'] == 'img':
                    vals['rssVideo'] = False
                    vals['urlVid'] = False
                elif vals['bannerPrincipalSelector'] == "rssVideo":
                    vals['bannerImg'] = False
                    vals['urlVid'] = False
                elif vals['bannerPrincipalSelector'] == "lvid":
                    vals['bannerImg'] = False
                    vals['videoField'] = False
        except:
            _logger.info("error write")

  

        return super(Event, self).write(vals)

    @api.constrains('description')
    def _constrains_description(self):
        if len(self.description) > 40000:
            raise exceptions.ValidationError(_("limite de caracteres 40000"))
        pass

    @api.constrains('title')
    def _constrains_title(self):
        if len(self.title) > 41:
            raise exceptions.ValidationError(_("limite de caracteres 41"))
        pass
