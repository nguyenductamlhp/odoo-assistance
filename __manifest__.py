# -*- coding: utf-8 -*-
{
    'name': "Tensorflow chat Odoo",

    'summary': "Tensorflow chat Odoo",

    'description': "Module Tensorflow chat Odoo",

    'author': "Tamnd",
    'website': "",
    'version': '1.0',
    'category': 'AI',

    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'views/ml_view.xml',
        'views/tf_predict_view.xml',
        'views/message/message_tag_view.xml',
    ],
}