# -*- coding: utf-8 -*-

from odoo import api, fields, models

class LeadLineBussiness(models.Model):
    _name = 'crm.lead.line.bussiness'
    _description = 'Linea de Negocio'

    name = fields.Char("Nombre",store=True)
    line_service_ids = fields.One2many("crm.lead.line.service","line_bussiness_id", string="Lineas de Servicio")

class LeadLineService(models.Model):
    _name = 'crm.lead.line.service'
    _description = 'Linea de Servicio'
    
    name = fields.Char("Nombre",store=True)
    line_bussiness_id = fields.Many2one("crm.lead.line.bussiness", string = "Linea de Negocio")

class LeadUnitService(models.Model):
    _name = 'crm.lead.unit.service'
    _description = 'Unidad de Servicio'

    name = fields.Char('Unidad de Servicio',store=True)
