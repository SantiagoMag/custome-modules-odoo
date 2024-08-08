# -*- coding: utf-8 -*-


from odoo import api, fields, models


class Lead(models.Model):
    _inherit = 'crm.lead'

    user_id = fields.Many2one(
        'res.users', string='Responsable Comercial', default=lambda self: self.env.user,
        domain="[('share', '=', False)]",
        check_company=True, index=True, tracking=True)
    
    user_proposal_id = fields.Many2one(
        'res.users', string='Responsable Propuesta', default=lambda self: self.env.user,
        domain="[('share', '=', False)]",
        check_company=True, index=True, tracking=True)
    
    tag_ids = fields.Many2many(
        'crm.tag', 'crm_tag_rel', 'lead_id', 'tag_id', string='Oferta Tentativa',
        help="Classify and analyze your lead/opportunity categories like: Training, Service")
    
    company_currency = fields.Many2one("res.currency", string='Moneda', store=True)

    line_bussiness_id = fields.Many2one('crm.lead.line.bussiness', string="Linea de Negocio")
    line_service_id = fields.Many2one('crm.lead.line.service', string="Linea de Servicio")
    unit_service_id = fields.Many2one('crm.lead.unit.service', string="Unidad de Negocio" )

    @api.depends('company_id')
    def _compute_company_currency(self):
        pass

    def action_view_sale_quotation(self):
        args = super(Lead,self).action_view_sale_quotation()
        print(args, flush=True)
        return args