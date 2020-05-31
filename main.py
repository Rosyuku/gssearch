# -*- coding: utf-8 -*-
"""
Created on Sun May 31 22:39:23 2020

@author: Wakasugi Kazuyuki
"""

import google_scholar_search 

if __name__ == "__main__":

    q = "machine learning"
    lr = "lang_en|lang_ja"
    as_ylo = 2018
    
    df = google_scholar_search.get_summary(q, lr=lr, as_ylo=as_ylo)