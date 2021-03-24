from odoo import fields,models,_,api,exceptions
class TotemConfigSettings(models.TransientModel):
    _inherit='res.config.settings'
    main_slider_control = fields.Float(string=_('main slider control'),related="company_id.mainSlider",readonly=False)
    secundary_slider_control=fields.Float(string=_(''),related="company_id.secundarySlider",readonly=False)
    description = fields.Text(string=_(''),related="company_id.description",readonly=False)
    companyQr = fields.Text(string=_(''),related="company_id.companyQr",readonly=False)
    prueba = fields.Integer(string='',related="company_id.prueba",readonly=False)
    @api.constrains('main_slider_control')  
    def _constrains_main_slider_control(self):
        if self.main_slider_control<1:
            raise ValidationError(_("el valor debe ser superior a uno"))
        pass

    @api.constrains('secundary_slider_control')
    def _constrains_secundary_slider_control(self):
        if self.secundary_slider_control<1:
            raise ValidationError(_("el valor debe ser superior a uno"))
        pass
    
   
    
   