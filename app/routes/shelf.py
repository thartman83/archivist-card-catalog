###############################################################################
## shelf.py for archivist card catalog microservice                        ##
## Copyright (c) 2023 Tom Hartman (thomas.lees.hartman@gmail.com)            ##
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
## Shelving routes
##
## }}}

### shelf ## {{{
import datetime
from flask import Blueprint, request, jsonify
from ..models import db, Shelf, RecordType, Collection

required_fields = ['record_type', 'title', 'filename', 'extension', 'author',
                       'checksum', 'size', 'user']

shelf_bp = Blueprint('shelf', __name__, url_prefix='/shelf')

@shelf_bp.route('', methods=['POST'])
def shelveCollection():
    json = request.get_json()

    # validate that the request has the required fields
    valid, res = validateRecordData(json)
    if not valid:
        return jsonify(res), 200

    user = json.pop('user', None)
    record_data = json.copy()
    record_data['creation_user'] = user
    record_data['edition'] = 1

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
        'collectionid': collection.collectionid,
    }, 200

@shelf_bp.route('/<int:id>', methods=['GET'])
def getRecord(id):
    collection = Collection.query.filter_by(collectionid = id).first()

    if collection is None:
        return {
            'Ok': False,
            'ErrMsg': 'Unknown collection {0}'.format(id)
        }, 200

    return {
        'Ok': True,
        'collection': collection.serialize()
    }

@shelf_bp.route('/<int:id>', methods=['POST'])
def addEdition(id):
    # check that the collectio supplied exists
    collection = Collection.query.filter_by(collectionid = id).first()
    if collection is None:
        return {
            'Ok': False,
            'ErrMsg': 'Unknown collection {0}'.format(id)
        }

    json = request.get_json()

    valid, res = validateRecordData(json)
    if not valid:
        return jsonify(res), 200

    newEditionNumber = collection.current_edition + 1

    user = json.pop('user', None)
    record_data = json.copy()
    record_data['creation_user'] = user
    record_data['edition'] = newEditionNumber
    record_data['collectionid'] = collection.collectionid

    try:
        record = Shelf(**record_data)

        collection.current_edition = newEditionNumber
        collection.modified_user = user
        collection.records.append(record)
        collection.modified_date = datetime.utcnow()
        db.session.add(record)
        db.session.commit()
    except:
        pass

    return {
        'Ok': True,
        'collection': collection.serialize()
    }, 200

@shelf_bp.route('/<int:id>/edition')
def getCollectionEditions(id):
    collection = Collection.query.filter_by(collectionid = id).first()
    if collection is None:
        return {
            'Ok': False,
            'ErrMsg': 'Unknown collection {0}'.format(id)
        }

    try:
        retval = {
            "Ok": True,
            "collectionid": collection.collectionid,
            "editions": list(map(lambda r: r.serialize(), collection.records))
        }
    except:
        return {
            "Ok": False,
            "ErrMsg": "Error occured while retrieving edition information"
        }, 200

    return retval, 200

@shelf_bp.route('/<int:collectionid>/edition/<int:editionid>')
def getEdition(collectionid, editionid):
    collection = Collection.query.filter_by(collectionid = collectionid).first()
    if collection is None:
        return {
            'Ok': False,
            'ErrMsg': 'Unknown collection {0}'.format(collectionid)
        }, 200

    edition = next(filter(lambda r: r.edition == editionid, collection.records),
                   None)

    if edition is None:
        return {
            'Ok': False,
            'Count': len(collection.records),
            'ErrMsg': 'Unknown edition {0}'.format(editionid)
        }, 200

    try:
        retval = {
            "collectionid": collection.collectionid,
            "Ok": True,
            "edition": edition.serialize()
        }
    except Exception as err:
        return {
            "Ok": False,
            "ErrMsg": f"Error retrieving edition {err=}"
        }, 200

    return retval, 200


def validateRecordData(json):
    ret = dict({ 'Ok': False, 'ErrMsg': []})
    valid = True

    # verify that it is a dictionary
    if not isinstance(json, dict):
        valid = False
        ret['ErrMsg'].append('Record data is not a dictionary')
        return valid, ret

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
