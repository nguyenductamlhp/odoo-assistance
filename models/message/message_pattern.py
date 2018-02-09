# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MessagePattern(models.Model):
    _description = 'Message Pattern'
    _name = 'message.pattern'

    name = fields.Char("Pattern Name")
    tag_id = fields.Many2one(
        'message.tag',
        string="Tag"
    )
