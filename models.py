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

from google.appengine.ext import db

class Wiki(db.Model):
    url =  db.StringProperty()
    author = db.UserProperty(auto_current_user_add=True)
    title = db.StringProperty()
    markdown = db.TextProperty()
    html = db.TextProperty()
    addtime = db.DateTimeProperty(auto_now=True)

    @staticmethod
    def get_by_url(url):
        wiki = Wiki.all().filter('url =', url.lower()).get()
        if not wiki:
            return Wiki.get_default_wiki(url.lower())
        return wiki

    @staticmethod
    def get_default_wiki(url):
        wiki = Wiki(url=url,
                title='Undefined!',
                markdown='**Page Not Exists!**',
                html='<p><strong>Page Not Exists!</strong></p>')
        return wiki

class Config(db.Model):
    name = db.StringProperty()
    value = db.StringProperty()

    @staticmethod
    def get_all_configs():
        configs = {}
        for config in Config.all():
            configs[config.name] = config.value
        if len(configs) == 0:
            configs = Config.get_default_configs()
        return configs

    @staticmethod
    def get_default_configs():
        return { 'theme' : 'default' }

    @staticmethod
    def update_configs(configs):
        for k, v in configs.items():
            config = Config.all().filter('name =', k).get()
            if not config:
                config = Config(name=k)
            config.value = v
            config.put()
