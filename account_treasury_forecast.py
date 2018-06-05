# -*- coding: utf-8 -*-
# © 2018 Tosin Komolafe @ Ballotnet Solutions Ltd <komolafetosin@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


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

    pledge_bank_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Pledge Bank')

    @api.multi
    def button_calculate(self):
        self.restart()
        self.calculate_invoices()
        self.calculate_line()
        self.calculate_cashflow()
        return True

    @api.one
    def calculate_invoices(self):
        invoice_obj = self.env['account.invoice']
        treasury_invoice_obj = self.env['account.treasury.forecast.invoice']
        new_invoice_ids = []
        in_invoice_lst = []
        out_invoice_lst = []
        state = []
        if self.check_draft:
            state.append("draft")
        if self.check_proforma:
            state.append("proforma")
        if self.check_open:
            state.append("open")
        invoice_ids = invoice_obj.search([('date_due', '>', self.start_date),
                                          ('date_due', '<', self.end_date),
                                          ('state', 'in', tuple(state))])
        for invoice_o in invoice_ids:
            values = {
                'invoice_id': invoice_o.id,
                'date_due': invoice_o.date_due,
                'partner_id': invoice_o.partner_id.id,
                'journal_id': invoice_o.journal_id.id,
                'state': invoice_o.state,
                'base_amount': invoice_o.amount_untaxed,
                'tax_amount': invoice_o.amount_tax,
                'total_amount': invoice_o.amount_total,
                'residual_amount': invoice_o.residual,
                'pledge_bank_id': invoice_o.pledge_bank_id.id
            }
            new_id = treasury_invoice_obj.create(values)
            new_invoice_ids.append(new_id)
            if invoice_o.type in ("out_invoice", "out_refund"):
                out_invoice_lst.append(new_id.id)
            elif invoice_o.type in ("in_invoice", "in_refund"):
                in_invoice_lst.append(new_id.id)
        self.write({'out_invoice_ids': [(6, 0, out_invoice_lst)],
                    'in_invoice_ids': [(6, 0, in_invoice_lst)]})
        return new_invoice_ids

class AccountTreasuryForecastLine(models.Model):
    _inherit = 'account.treasury.forecast.line'

    forecast_bank_id = fields.Many2one(
        comodel_name='res.partner.bank', 
        string='Forecast Bank')
