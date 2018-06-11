# -*- coding: utf-8 -*-
# © 2018 Salvador Sanjuan @ Acelerem salvador@aceleratuempresa.net
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
    def calculate_cashflow(self):
        result = super(AccountTreasuryForecast, self).calculate_cashflow()
        for cashflow_o in self.cashflow_ids:
            pledge_bank_id = cashflow_o.template_line_id.invoice_id.pledge_bank_id.id
            cashflow_o.pledge_bank_id = pledge_bank_id
        return result

    @api.one
    def calculate_invoices(self):
        invoice_obj = self.env['account.invoice']
        treasury_invoice_obj = self.env['account.treasury.forecast.invoice']
        new_invoice_ids = []
        in_invoice_lst = []
        out_invoice_lst = []
        state = []
        payment_status = False
        if self.check_draft:
            state.append("draft")
        if self.check_proforma:
            state.append("proforma")
        if self.check_open:
            state.append("open")
        if self.check_pledged:
            invoice_ids = invoice_obj.search([('date_due', '>', self.start_date),
                                          ('date_due', '<', self.end_date),
                                          '|', ('state', 'in', tuple(state)),
                                          ('payment_status','=', 'pledged')])
        else:
            invoice_ids = invoice_obj.search([('date_due', '>', self.start_date),
                                          ('date_due', '<', self.end_date),
                                          ('state', 'in', tuple(state)),
                                          ('payment_status','!=', 'pledged')])
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


    @api.one
    def calculate_line(self):
        line_obj = self.env['account.treasury.forecast.line']
        temp_line_obj = self.env['account.treasury.forecast.line.template']
        new_line_ids = []
        temp_line_lst = temp_line_obj.search([('treasury_template_id', '=',
                                               self.template_id.id)])
        for line_o in temp_line_lst:
            if ((line_o.date > self.start_date and
                    line_o.date < self.end_date) or
                    not line_o.date) and not line_o.paid:
                values = {
                    'name': line_o.name,
                    'date': line_o.date,
                    'line_type': line_o.line_type,
                    'partner_id': line_o.partner_id.id,
                    'template_line_id': line_o.id,
                    'amount': line_o.amount,
                    'pledge_bank_id':line_o.invoice_id.pledge_bank_id.id,
                    'treasury_id': self.id,
                }
                new_line_id = line_obj.create(values)
                new_line_ids.append(new_line_id)
        return new_line_ids

class AccountTreasuryForecastLine(models.Model):
    _inherit = 'account.treasury.forecast.line'

    pledge_bank_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Pledge Bank')

    forecast_bank_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Forecast Bank')

class AccountTreasuryForecastLineTemplate(models.Model):
    _inherit = 'account.treasury.forecast.line.template'

    pledge_bank_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Pledge Bank')

class AccountTreasuryForecastCashflow(models.Model):
    _inherit = "account.treasury.forecast.cashflow"

    pledge_bank_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Pledge Bank')
