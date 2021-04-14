
from odoo import models, fields, api, _, exceptions
import logging


_logger = logging.getLogger(__name__)


class Horas(models.Model):
    _name = 'event.time'
    name = fields.Text(string='')
    horaInicial = fields.Float(string=_(''), digits=(2, 2))
    horaFinal = fields.Float(string=_(''),digits=(2,2)) 