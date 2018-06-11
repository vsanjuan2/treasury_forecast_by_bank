# -*- coding: utf-8 -*-
# © 2018 TSalvador Sanjuan @ Acelerem salvador@aceleratuempresa.net
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name' : 'Acelerem Account Tresury Forecast',
    'version' : '1.0',
    'author' : 'Acelerem',
    'category' : 'Accounting & Finance',
    'description' : """
Chimpex Accounting and Financial Management.
====================================
   This module manages the treasury forecast.
        Calculates the treasury forecast from supplier and customer invoices,
        recurring payments and variable payments.
    """,
    'website': 'odoo.acelerem.com',
    'depends' : ['account_treasury_forecast_banking', 'account_treasury_forecast_cashflow_banking'],
    'data': [
        'views/account_treasury_forecast_view.xml',
        'report/account_treasury_forecast_analysis_view.xml'
    ],
    'qweb' : [],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
