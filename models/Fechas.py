
from odoo import models, fields, api, _, exceptions
import logging
import re
from datetime import *

_logger = logging.getLogger(__name__)


class Fechas(models.Model):
    _name = 'event.date'
    name = fields.Text(string=_(''))
    fecha = fields.Date(string=_(''))
    rangoHoras = fields.Many2many('event.time', string='')
    events = fields.Many2one('event.totem', string='')
