# -*- coding: utf-8 -*-
# © 2018 Tosin Komolafe @ Ballotnet Solutions Ltd <komolafetosin@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name' : 'Chimpex Account Tresury Forecast',
    'version' : '1.0',
    'author' : 'Chimpex Solutions Ltd',
    'category' : 'Accounting & Finance',
    'description' : """
Chimpex Accounting and Financial Management.
====================================
   This module manages the treasury forecast.
        Calculates the treasury forecast from supplier and customer invoices,
        recurring payments and variable payments.
    """,
    'website': 'tosinkomolafe.com',
    'depends' : ['account_treasury_forecast'],
    'data': [
        'views/account_treasury_forecast_view.xml',
     
    ],
    'qweb' : [],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}