#
# refer to http://flask.pocoo.org/docs/0.10/quickstart/
#

import os
from flask import Flask
from flask.ext.cache import Cache

from criteria import criteria_blueprint
from raw import raw_blueprint
from result import result_blueprint
from auth import auth
from flask.templating import render_template

app = Flask(__name__)


def create_app(app_name='dcsqa', config='config.DevelopmentConfig'):
    app.config.from_object(config)
    app.cache = Cache(app) 

    # register blueprint for each restful entry
    # http://flask.pocoo.org/docs/0.10/blueprints/
    app.register_blueprint(criteria_blueprint, url_prefix='/criteria')
    app.register_blueprint(raw_blueprint, url_prefix='/raw')
    app.register_blueprint(result_blueprint, url_prefix='/result')

    return app


@app.route('/')
def index():
    return 'please use API'


@app.route('/login')
@auth.login_required
def login():
    return 'welcome!'

@app.route('/env')
@auth.login_required
def env():
    return render_template('env.html', env=os.environ)