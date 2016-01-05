#!/usr/bin/python
from flask import Flask, request

import latex2mathml

__author__ = 'Ronie Martinez'

DEBUG = True
app = Flask(__name__)


@app.route('/')
def index():
    latex = request.args.get('latex')
    if latex:
        return '<p>{}</p>'.format(latex2mathml.convert(latex))
    return 'LaTeX code not found!'


if __name__ == '__main__':
    app.run()