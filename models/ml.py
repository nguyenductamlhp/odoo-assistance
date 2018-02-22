# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError
import os
import json


import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
 
import numpy as np
import tflearn
import tensorflow as tf
import random
import pickle


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
        lst_dir = []
        lst_dir = path.split('/')
        lst_dir.pop()
        file_path = '/'.join(lst_dir) + '/intents.json'
        with open(file_path, 'wb') as outfile:
            json.dump(dict, outfile)

    def training(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        lst_dir = []
        lst_dir = path.split('/')
        lst_dir.pop()
        module_path = '/'.join(lst_dir) + '/'
        with open(module_path + 'intents.json') as json_data:
            intents = json.load(json_data)
        
        words = []
        classes = []
        documents = []
        ignore_words = ['?']
        
        for intent in intents['intents']:
            for pattern in intent['patterns']:
        
                w = nltk.word_tokenize(pattern)
                words.extend(w)
                documents.append((w, intent['tag']))
                if intent['tag'] not in classes:
                    classes.append(intent['tag'])
        
        words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
        words = sorted(list(set(words)))
        
        classes = sorted(list(set(classes)))
        
        print (len(documents), "documents")
        print (len(classes), "classes", classes)
        print (len(words), "unique stemmed words", words)
        #Create training data
        training = []
        output = []
        
        output_empty = [0] * len(classes)
        
        for doc in documents:
            bag = []
            pattern_words = doc[0]
            pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
        
            for w in words:
                bag.append(1) if w in pattern_words else bag.append(0)
        
            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1
        
            training.append([bag, output_row])
        
        random.shuffle(training)
        training = np.array(training)
        
        train_x = list(training[:,0])
        train_y = list(training[:,1])
        print(train_x[1])
        print(train_y[1])
        
        tf.reset_default_graph()
        
        net = tflearn.input_data(shape=[None, len(train_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
        net = tflearn.regression(net, optimizer='adam', loss='categorical_crossentropy')
        
        model = tflearn.DNN(net, tensorboard_dir=module_path + 'data/tflearn_logs')
        
        model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
        model.save(module_path + 'data/model.tflearn')
        
        pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open(module_path + "data/training_data", "wb" ) )