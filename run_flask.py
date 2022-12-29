# -*- encoding: utf-8 -*-

"""
Copyright (c) 2022 - present localhost
"""
from importlib import import_module

from flask import Flask


def register_blueprints(app):
    # for module_name in (['home']):

    module = import_module('home.routes')

    app.register_blueprint(module.blueprint)


def create_app():
    app = Flask(__name__)
    register_blueprints(app)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
