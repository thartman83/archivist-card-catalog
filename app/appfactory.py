###############################################################################
#  appfactory.py for archivist card catalog microservice                      #
#  Copyright (c) 2022 Tom Hartman (thomas.lees.hartman@gmail.com)             #
#                                                                             #
#  This program is free software; you can redistribute it and/or              #
#  modify it under the terms of the GNU General Public License                #
#  as published by the Free Software Foundation; either version 2             #
#  of the License, or the License, or (at your option) any later              #
#  version.                                                                   #
#                                                                             #
#  This program is distributed in the hope that it will be useful,            #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#  GNU General Public License for more details.                               #
###############################################################################

# Module DocString {{{
"""
Appfactory pattern implemention
"""
# }}}

# appfactory # {{{
from flask import Flask
from flask_cors import CORS
from .routes.status import status_bp, init_bp
from .routes.tag import tag_bp
from .routes.shelf import shelf_bp
from .models.dbbase import db


def create_app(cfg):
    """Create a archivist card catalog

    Keyword arguments:
    cfg -- configuration object
    """
    app = Flask(__name__)
    app.config.from_object(cfg)
    db.init_app(app)

    # register the route blueprints
    app.register_blueprint(status_bp)
    app.register_blueprint(init_bp)
    app.register_blueprint(shelf_bp)
    app.register_blueprint(tag_bp)

    # enable cors support
    CORS(app)

    return app
# }}}
