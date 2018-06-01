# -*- coding: utf-8 -*-
# © 2018 Tosin Komolafe @ Ballotnet Solutions Ltd <komolafetosin@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountTreasuryForecastInvoice(models.Model):
    _inherit = 'account.treasury.forecast.invoice'

    pledge_bank_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Pledge Bank')

    forecast_bank_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Forecast Bank')


class AccountTreasuryForecast(models.Model):
    _inherit = 'account.treasury.forecast'

    check_pledged = fields.Boolean(
        string='Pledged')

class AccountTreasuryForecastLine(models.Model):
    _inherit = 'account.treasury.forecast.line'

    forecast_bank_id = fields.Many2one(
        comodel_name='res.partner.bank', 
        string='Forecast Bank')
