###############################################################################
## appfactory.py for archivist card catalog microservice                     ##
## Copyright (c) 2022 Tom Hartman (thomas.lees.hartman@gmail.com)            ##
##                                                                           ##
## This program is free software; you can redistribute it and/or             ##
## modify it under the terms of the GNU General Public License               ##
## as published by the Free Software Foundation; either version 2            ##
## of the License, or the License, or (at your option) any later             ##
## version.                                                                  ##
##                                                                           ##
## This program is distributed in the hope that it will be useful,           ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of            ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             ##
## GNU General Public License for more details.                              ##
###############################################################################

### Commentary ## {{{
##
## Appfactory pattern implemention
##
## }}}

### appfactory ## {{{
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .routes.status import status_bp
from .models.dbbase import db

class AppConfig:
    dbEngine = ""
    dbHost = ""
    dbName = ""
    dbUser = ""
    dbPasswd = ""
    storageLocation = ""

def create_app(cfg):
    app = Flask(__name__)
    app.config.from_object(cfg)
    db.init_app(app)

    # register the route blueprints
    app.register_blueprint(status_bp)

    # enable cors support
    CORS(app)

    return app

## }}}
