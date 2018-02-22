# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError
import os
import json


class ML(models.Model):
    _description = 'Machine Learning'
    _name = 'machine.learning'


    name = fields.Char("Machine name")
    
    def generate_tag(self):
        act_env = self.env['ir.actions.act_window']
        menu_env = self.env['ir.ui.menu']
        param_env = self.env['ir.config_parameter']
        
        pattern_env = self.env['message.pattern']
        tag_env = self.env['message.tag']
        response_env = self.env['message.response']
        
        acts = act_env.search([])
        for act in acts:
            print act.id, act.name
            # create pattern
            val_pat = {
                'name': act.name
            }
            pat = pattern_env.create(val_pat)
            # create response
            url = "/web?#min=1&limit=80"
            if act.res_id:
                url = url + 'id=%s' % act.res_id
            if act.res_model:
                url = url + '&model=%s' % act.res_model
            url = url + '&action=%s' % act.id
            val_res = {
                'name': param_env.get_param('web.base.url') + url
            }
            resp = response_env.create(val_res)
            # Create tag
            val_tag = {
                'name': act.name,
            }
            tag = tag_env.create(val_tag)
            # Relational mapping
            pat.tag_id = tag.id
            resp.tag_id = tag.id

    def parse_data_to_json(self):
        tag_env = self.env['message.tag']
        tags = tag_env.search([])
        dict = {}
        intents = []
        for tag in tags:
            pattern = [p.name for p in tag.pattern_ids]
            response = [p.name for p in tag.response_ids]
            item = {
                'tag': tag.name,
                'patterns': pattern,
                'responses': response,
            }
            intents.append(item)
        dict['intents'] = intents
        
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        print "path", path, type(path)
        lst_dir = []
        lst_dir = path.split('/')
        lst_dir.pop()
        file_path = '/'.join(lst_dir) + '/intents.json'
        with open(file_path, 'wb') as outfile:
            json.dump(dict, outfile)
        # with open(file) as infile:
        #     data = json.load(infile)