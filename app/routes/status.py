###############################################################################
## status.py for archivist card catalog microservice                        ##
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
## Status routes
##
## }}}

### status ## {{{
from flask import Blueprint, request, jsonify, current_app
from ..models.dbbase import db

status_bp = Blueprint('status', __name__, url_prefix='/status')

@status_bp.route('', methods=['GET'])
def getStatus():
    res = dict()
    dbInfo = dict({'tables': db.metadata.tables})
    if len(dbInfo['tables']) == 0:
        dbInfo['status'] = 'Uninitialized'
    else:
        dbInfo['status'] = 'Initialized'
    res['database'] = dbInfo

    return jsonify(res), 200

## }}}
