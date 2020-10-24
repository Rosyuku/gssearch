# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 12:09:31 2019

@author: m162109
"""

# Flask などの必要なライブラリをインポートする
import os
import sys
from flask import Flask, render_template, request, redirect, url_for
#from werkzeug.utils import secure_filename
from waitress import serve

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import google_scholar_search
from gvalue import Gvalue

class settings:
    pass
    
# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)
app.config.from_object(settings)
gvalue = Gvalue(app)

# / にアクセスしたときの処理
@app.route('/')
def root():
    return redirect(url_for('top'))

# top にアクセスしたときの処理
@app.route('/top', methods=['GET', 'POST'])
def top():
    title = "Google Scholar Search"
    
    if request.method == 'POST':

        query = request.form['query']
        lr = request.form['lr']
        as_ylo = request.form['as_ylo']
        as_yhi = request.form['as_yhi']
        scisbd = request.form['scisbd']
        as_vis = request.form['as_vis']
        as_sdt = request.form['as_sdt']
        num = request.form['num']

        print('query:{}, lr:{}, as_ylo:{}, as_yhi:{}, scisbd:{}, as_vis:{}, as_sdt:{}, num:{}'.format(query, lr, as_ylo, as_yhi, scisbd, as_vis, as_sdt, num))
        
        df_result, response_text = google_scholar_search.get_summary(query, 
                                                      lr=lr, 
                                                      as_ylo=as_ylo,
                                                      as_yhi=as_yhi,
                                                      scisbd=scisbd,
                                                      as_vis=as_vis,
                                                      as_sdt=as_sdt,
                                                      num=int(num),
                                                      )
        df_result = df_result.sort_values('citations', ascending=False)
        print(df_result.head())
        if df_result.shape[0] > 0:
            message = 'Search success'
        else:
            message = response_text
        
        print(query)
        
        return render_template('top.html', 
                               title=title,
                               query=query,
                               lr=lr,
                               as_ylo=as_ylo,
                               as_yhi=as_yhi,
                               scisbd=scisbd,
                               as_vis=as_vis,
                               as_sdt=as_sdt,
                               num=num,
                               dfflag=True,
                               df_index=df_result.index.tolist(),
                               df_columns=df_result.columns.tolist(),
                               df=df_result.values,
                               message=message,
                               )

        
    else:
        return render_template('top.html',
                               title=title,
                               )

if __name__ == '__main__':
    # app.debug = True # デバッグモード有効化
    # app.run(host='0.0.0.0', port=8080, threaded=False) # どこからでもアクセス可能に
    serve(app, host='0.0.0.0', port=8080)
