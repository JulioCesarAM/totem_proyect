# -*- coding: utf-8 -*- 
from odoo import http


class TotemProyect(http.Controller):
    @http.route('/totem_proyect/totem_proyect/', auth='public')
    def index(self, **kw):
        return http.request.render('totem_proyect.eventView', {
          #  'root': '/totem_proyect/totem_proyect',
            'objects': http.request.env['event.totem'].search([]),
       })

    @http.route('/totem_proyect/totem_proyect/objects/', auth='public')
    def list(self, **kw):

        return 'hola'

    @http.route('/totem_proyect/totem_proyect/objects/<model("totem_proyect.totem_proyect"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('totem_proyect.object', {
            'object': obj
        })
