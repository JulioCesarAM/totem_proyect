from odoo import fields,models,_,api
class TotemConfigSettings(models.TransientModel):
    _inherit='res.config.settings'
    #totem_proyect_img_slider_control = fields.Float(string=_(''), related="Event.sliderImgTimer")
    totem_proyect_img_slider_control = fields.Float(string=_(''))
    principal_slider_timer = fields.Float(string=_(''))
    def set_values(self):
        res = super(TotemConfigSettings,self).set_values()
        self.env['ir.config_parameter'].set_param('totem_proyect.totem_proyect_img_slider_control',self.totem_proyect_img_slider_control)
        return res
    
    @api.model
    def get_values(self):
        res = super(TotemConfigSettings,self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        controls=ICPSudo.get_param('totem_proyect.totem_proyect_img_slider_control')
        res.update(
            totem_proyect_img_slider_control=controls
        )
        return res

