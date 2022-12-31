###############################################################################
## record.py for archivist card catalog routes                              ##
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
## record routes
##
## }}}

### record ## {{{
from flask import Blueprint, request, jsonify
from ..models import Shelf, RecordType

required_fields = ['record_type', 'title', 'filename', 'extension', 'author',
                       'checksum', 'size', 'user']

record_bp = Blueprint('record', __name__, url_prefix='/record')

@record_bp.route('', methods=['POST'])
def createRecord():
    json = request.get_json()

    # validate that the request has the required fields
    valid, res = validateRecordData(json)
    if not valid:
        return jsonify(res), 200

    user = json.pop('user', None)
    json['current_version'] = 1
    json['creation_user'] = user
    json['modification_user'] = user

    record = Shelf(**json)
    db.session.add(record)
    db.session.commit()


def validatRecordData(json):
    ret = dict({ 'Ok': False, 'ErrMsg': []})
    valid = True

    # check the json data for the following keys
    keys = list(json.keys())
    for field in required_fields:
        if field not in keys:
            valid = False
            ret['ErrMsg'].append('Missing {0} field'.format(field))

    # check that the record type is a number
    if 'record_type' in json and not isinstance(json['record_type'], int):
        valid = False
        ret['ErrMsg'].append('record_type is not valid')
    elif 'record_type' in json:
        # check that the record type is one of the currently defined ones
        recordType = int(json['record_type'])
        if len(list(filter(lambda e: e.value == recordType, list(RecordType)))) <= 0:
            valid = False
            ret['ErrMsg'].append('Unknown record type {0}'.format(recordType))

    if not valid:
        return valid, ret
    else:
        return valid, {}

## }}}
