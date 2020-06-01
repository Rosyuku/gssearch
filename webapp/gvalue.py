# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 12:11:27 2019

@author: m162109
"""

import os
import pandas as pd

class Gvalue(object):
    def __init__(self, app=None, model=None):
        self.init_app(app)

    def init_app(self, app):
        # configを見て何かする
        print(app.config)

