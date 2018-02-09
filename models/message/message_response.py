# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MessageResponse(models.Model):
    _description = 'Message Response'
    _name = 'message.response'

    name = fields.Char("Response Name")
    tag_id = fields.Many2one(
        'message.tag',
        string="Tag"
    )
