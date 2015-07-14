#!/bin/env python
# coding: utf-8

from flask import Flask
from criteria import criteria_blueprint
from raw import raw_blueprint

app = Flask(__name__)


def create_app(app_name='dcsqa', config='config.DevelopmentConfig'):
    app.config.from_object(config)

    # register blueprint for each restful entry
    app.register_blueprint(criteria_blueprint, url_prefix='/criteria')
    app.register_blueprint(raw_blueprint, url_prefix='/raw')

    return app


@app.route('/')
def index():
    return 'please use API'