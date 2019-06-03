# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 10:39:27 2019

@author: barak
"""

from sentence_parser import syntesize_sentence
from flask import Flask, request
#import requests

IP = "127.0.0.1"
PORT = 3000

app = Flask(__name__)

@app.route("/parse_sentence", methods=['POST'])
def sentence_analyzer():
 #   print(request.form['sentence'])
    sentence_request = syntesize_sentence(request.form['sentence'])
    request_url = "https://%s:%d"%(IP, PORT)
    request_url = request_url+"/%s"
    if(sentence_request['action'] != " " and sentence_request['object'] != " "):
        action = sentence_request['action'] 
        sentence_object =  sentence_request['object']
        request_url = request_url+"/%s"
        request_url = request_url % (action, sentence_object)
        if(sentence_request['value'] != {'val':'zero'}):
            request_url = request_url+"?%s"
            params = ["%s=%s" % (field, value)
                            for field, value in sentence_request['value'].items()]
            params_string = "&".join(params)
            request_url = request_url % (params_string)

    else:
        request_url = request_url % ("error")
 #   r = requests.post(url = request_url)
    return request_url

app.run()