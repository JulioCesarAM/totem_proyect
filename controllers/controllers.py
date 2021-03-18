# -*- coding: utf-8 -*-
from odoo import http

# class TotemProyect(http.Controller):
#     @http.route('/totem_proyect/totem_proyect/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/totem_proyect/totem_proyect/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('totem_proyect.listing', {
#             'root': '/totem_proyect/totem_proyect',
#             'objects': http.request.env['totem_proyect.totem_proyect'].search([]),
#         })

#     @http.route('/totem_proyect/totem_proyect/objects/<model("totem_proyect.totem_proyect"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('totem_proyect.object', {
#             'object': obj
#         })