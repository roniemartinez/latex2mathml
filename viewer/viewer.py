#!/usr/bin/python
from flask import Flask, request, render_template

import latex2mathml

__author__ = 'Ronie Martinez'

DEBUG = True
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    latex = request.form.get('latex')
    if latex:
        return '<p>{}</p>'.format(latex2mathml.convert(latex))
    return 'LaTeX code not found!'


if __name__ == '__main__':
    app.run()
