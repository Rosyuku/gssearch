# -*- coding: utf-8 -*-
"""
Created on Sun May 31 00:23:02 2020

@author: Wakasugi Kazuyuki

#Works Cited
https://own-search-and-study.xyz/2019/06/09/python-scraping-icml2019-summary/
https://serpapi.com/google-scholar-api
https://qiita.com/kuto/items/9730037c282da45c1d2b
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def get_summary(q, 
               lr="",
               as_ylo="",
               as_yhi="",
               scisbd=0,
               as_vis=1,
               as_sdt=1,
               num=100
               ):
    """
    q:Parameter defines the query you want to search.
    lr:Search langages (ex: lang_en|lang_jp)
    as_ylo:Parameter defines the year from which you want the results to be included. 
    as_yhi:Parameter defines the year until which you want the results to be included.
    scisbd:0 - Sort by relevance, 1 - Sort by date
    as_vis::0 - include citations. 1 - exclude citations.
    as_sdt:0 - include patents. 1 - exclude patents.
    num:maximum number of results to return (max:100)
    """
    
    params = dict()
    params["q"] = q
    params["lr"] = lr
    params["as_ylo"] = as_ylo
    params["as_yhi"] = as_yhi
    params["scisbd"] = scisbd
    params["as_vis"] = as_vis
    params["as_sdt"] = as_sdt
    params["hl"] = "ja"
    params["num"] = min(100, num)

    columns = ["rank", "title", "abust", "writer", "year", "citations", "url"]
    df = pd.DataFrame(columns=columns) #表の作成
    
    url_base  = "https://scholar.google.co.jp/scholar?"
    url_get = "q=" + "+".join(params["q"].split(" "))
    for key in params.keys():
        url_get += '&' + key + '=' + str(params[key])  
    url = url_base + url_get

    for start in range(0, params["num"], 20):
        
        session = requests.session()
        response = session.get(url + '&start=' + str(start))
        soup = BeautifulSoup(response.text, "html.parser")
        
        tags1 = soup.find_all("h3", {"class": "gs_rt"})  # title&url
        tags2 = soup.find_all("div", {"class": "gs_a"})  # writer&year
        tags3 = soup.find_all(text=re.compile("引用元"))  # citation
        tags4 = soup.find_all("div", {"class": "gs_rs"})
    
        rank = start + 1
        for tag1, tag2, tag3, tag4 in zip(tags1, tags2, tags3, tags4):
            title = tag1.text.replace("[HTML]","")
            aurl = tag1.select("a")[0].get("href")
            writer = tag2.text
            writer = re.sub(r'\d', '', writer)
            year = tag2.text
            year = re.sub(r'\D', '', year)[-4:]
            citations = tag3.replace("引用元","")
            abust = tag4.text
            se = pd.Series([rank, title, abust, writer, int(year), int(citations), aurl], columns)
            df = df.append(se, columns)
            rank += 1
            
    return df

if __name__ == "__main__":

    q = "machine learning"
    lr = "lang_en|lang_ja"
    as_ylo = 2018
    
    df = get_summary(q, lr=lr, as_ylo=as_ylo)
    

