# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 10:39:27 2019

@author: barak
"""

from __future__ import unicode_literals

from sentence_parser import syntesize_sentence
from flask import Flask, request
from flask import jsonify
#import requests


#IP = "127.0.0.1"
#PORT = 3000

app = Flask(__name__)

@app.route("/parse_sentence", methods=['POST'])
def sentence_analyzer():
    sentence_request = syntesize_sentence(request.form['sentence'])
    return jsonify(sentence_request)

if __name__ == "__main__":
    app.run()

