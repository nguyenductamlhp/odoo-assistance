# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MessageTag(models.Model):
    _description = 'Message Tag'
    _name = 'message.tag'

    name = fields.Char("Tag Name")
    pattern_ids = fields.One2many(
        'message.pattern', 'tag_id',
        string="Patterns"
    )
    response_ids = fields.One2many(
        'message.response', 'tag_id',
        string="Responses"
    )
