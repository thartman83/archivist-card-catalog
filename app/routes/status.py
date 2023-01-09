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
from sqlalchemy import desc
from ..models import db, CardCatalog
from ..version import VERSION, APPNAME


status_bp = Blueprint('status', __name__, url_prefix='/status')

@status_bp.route('', methods=['GET'])
def getStatus():
    res = dict()
    dbInfo = dict()

    try:
        rec = CardCatalog.query.order_by(desc(CardCatalog.version)).first()
        if rec is None:
            dbInfo['status'] = 'Uninitialized'
            dbInfo['errMsg'] = 'Application version not found'
        else:
            dbInfo['status'] = 'Initialized'
            dbInfo = {**dbInfo, **(rec.serialize()) }

    except Exception as err:
        dbInfo['status'] = 'Uninitialized'
        dbInfo['errMsg'] = 'Error retrieving application version: "{0}"'.format(err)

    res['database'] = dbInfo
    print(res)
    return jsonify(res), 200

init_bp = Blueprint('init', __name__, url_prefix='/init')

@init_bp.route('', methods=['POST'])
def initializeDatabase():
    rec = None
    dbExists = False

    # Check to see if the application table has existing entries
    try:
        rec = CardCatalog.query.order_by(desc(CardCatalog.version)).first()
        dbExists = True
    except:
        dbExists = False
        rec = None

    if rec is not None:
        return { 'Ok': False,
                 'ErrMsg': 'Database already initialized with version {0}'.format(rec.version)}, 200

    # If the query above fails the database has not been created
    if dbExists == False:
        try:
            db.create_all()
        except:
            return { 'Ok': False,
                     'ErrMsg': 'Error creating database' }, 200
    # Add the application information to the application table
    try:
        newRec = CardCatalog(name=APPNAME,version=VERSION)
        db.session.add(newRec)
        db.session.commit()

        return { 'Ok': True,
                 'response': newRec.serialize() }, 200
    except Exception as err:
        return { 'Ok': False,
                 'ErrMsg': 'Error initializing application version: {0}'.format(err) }, 200

## }}}
