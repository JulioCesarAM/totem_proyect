from odoo import fields,models,_,api,exceptions
class TotemConfigSettings(models.TransientModel):
    _inherit='res.config.settings'
    main_slider_control = fields.Float(string=_('main slider control'),related="company_id.mainSlider")
    secundary_slider_control=fields.Float(string=_(''),related="company_id.secundarySlider")
    description = fields.Text(string=_(''),related="company_id.description")
    companyQr = fields.Text(string=_(''),related="company_id.companyQr")
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
    
   
    
   