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
from ..models import db, Shelf, RecordType, Collection

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
    record_data = json.copy()
    record_data['creation_user'] = user

    collection_data = {
        "current_edition": 1,
        "creation_user": user,
        "modified_user": user
    }

    try:
        collection = Collection(**collection_data)

        record_data['collectionid'] = collection.collectionid
        record = Shelf(**record_data)

        collection.records.append(record)
        db.session.add(record)
        db.session.commit()
    except Exception as err:
        return {
            'Ok': False,
            'ErrMsg': 'Error commiting record "{0}"'.format(err)
        }, 200

    return {
        'Ok': True,
        'recordid': record.recordid
    }, 200

## }}}
