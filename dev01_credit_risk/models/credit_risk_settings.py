from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    """
        Configuración de H2O
    """

    h2o_driverless_address = fields.Char(string='URL', store=True, config_parameter="dev01_credit_risk.h2o_driverless_address")
    h2o_driverless_username = fields.Char(string='Username', store=True, config_parameter="dev01_credit_risk.h2o_driverless_username")
    h2o_driverless_password = fields.Char(string='Password', store=True, config_parameter="dev01_credit_risk.h2o_driverless_password")
    h2o_driverless_name_experiment = fields.Char(string='Nombre Experimento', store=True, config_parameter="dev01_credit_risk.h2o_driverless_name_experiment")

    """
        Configuración de VM
    """
    api_vm_url = fields.Char(string='API URL', store=True, config_parameter="dev01_credit_risk.api_vm_url")
    
    @api.model
    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].set_param('dev01_credit_risk.h2o_driverless_address', self.h2o_driverless_address)
        self.env['ir.config_parameter'].set_param('dev01_credit_risk.h2o_driverless_username', self.h2o_driverless_username)
        self.env['ir.config_parameter'].set_param('dev01_credit_risk.h2o_driverless_password', self.h2o_driverless_password)
        self.env['ir.config_parameter'].set_param('dev01_credit_risk.h2o_driverless_name_experiment', self.h2o_driverless_name_experiment)
        self.env['ir.config_parameter'].set_param('dev01_credit_risk.api_vm_url', self.api_vm_url)

    @api.model
    def get_values(self):
        res = super().get_values()
        res['h2o_driverless_address']       = self.env['ir.config_parameter'].sudo().get_param('dev01_credit_risk.h2o_driverless_address')
        res['h2o_driverless_username'] = self.env['ir.config_parameter'].sudo().get_param('dev01_credit_risk.h2o_driverless_username')
        res['h2o_driverless_password'] = self.env['ir.config_parameter'].sudo().get_param('dev01_credit_risk.h2o_driverless_password')
        res['h2o_driverless_name_experiment'] = self.env['ir.config_parameter'].sudo().get_param('dev01_credit_risk.h2o_driverless_name_experiment')
        res['api_vm_url'] = self.env['ir.config_parameter'].sudo().get_param('dev01_credit_risk.api_vm_url')

        return res

    