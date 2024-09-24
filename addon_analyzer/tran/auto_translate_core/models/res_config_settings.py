# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TranslatorConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    # is_extra = fields.Boolean(string='Apply Extra Amount',
    #                           config_parameter='venue_booking_management.is_extra',
    #                           help="Enable, if extra charge want to add")

    translation_service = fields.Selection([
        ('google', 'Google Translate')
    ], string="Default Translation Service",config_parameter='auto_translate_core.translation_service')

    # def set_values(self):
    #     super(TranslatorConfigSettings, self).set_values()
    #     self.env['ir.config_parameter'].sudo().set_param(
    #         'auto_translate_core.default_translation_service', self.default_translation_service)
    #
    # @api.model
    # def get_values(self):
    #     res = super(TranslatorConfigSettings, self).get_values()
    #     res.update(
    #         default_translation_service=self.env['ir.config_parameter'].sudo().get_param('auto_translate_core.default_translation_service', default='google')
    #     )
    #     return res