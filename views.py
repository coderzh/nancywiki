#!/usr/bin/env python
#coding:utf-8
#
# Copyright 2010 CoderZh.com.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'CoderZh'

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

from models import *

class BaseRequestHandler(webapp.RequestHandler):
    def template_render(self, template_name, template_values = {}):
        config = Config.get_all_configs()
        directory = os.path.dirname(__file__)
        template_path = os.path.join(directory, 'themes', config['theme'], template_name)
        user = users.get_current_user()
        logout_url = users.create_logout_url(self.request.uri)
        login_url = users.create_login_url(self.request.uri)
        values = { 'config' : config,
                'user' : user,
                'logout_url' : logout_url,
                'login_url' : login_url
                }
        values.update(template_values)
        self.response.out.write(template.render(template_path, values).decode('utf-8'))
        
class WikiPageHandler(BaseRequestHandler):
    def get(self, url):
        wiki = Wiki.get_by_url(url)
        editmode = self.request.get('edit')
        is_demo = url == 'demo'
        if editmode == '1':
            if is_demo or users.is_current_user_admin():
                self.template_render('edit.html', { 'wiki' : wiki })
            else:
                login_url = users.create_login_url(self.request.uri)
                self.redirect(login_url)
        else:
            self.template_render('wiki.html', { 'wiki' : wiki })

    def post(self, url):
        is_demo = url == 'demo'
        if is_demo or users.is_current_user_admin():
            wiki = Wiki.get_by_url(url)
            wiki.title = self.request.get('title')
            wiki.markdown = self.request.get('markdown')
            wiki.html = self.request.get('html')
            wiki.author = users.get_current_user()
            wiki.put()
        self.redirect('/' + url)

class ConfigPageHandler(BaseRequestHandler):
    def get(self):
        if users.is_current_user_admin():
            self.template_render('config.html')
        else:
            self.redirect('/')

    def post(self):
        if users.is_current_user_admin():
            configs = { 
                'theme' : self.request.get('theme'),
                'domain' : self.request.get('domain'),
                'title' : self.request.get('title'),
            }
            Config.update_configs(configs)
            self.redirect('/config/')
        else:
            self.redirect('/')
