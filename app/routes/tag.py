###############################################################################
## tag.py for archiivist card catalog microservice                       ##
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
## Tag routes
##
## }}}

### tag ## {{{
import datetime
from flask import Blueprint, request, jsonify
from ..models import db, Tag

tag_bp = Blueprint('tag', __name__, url_prefix='/tag')

@tag_bp.route('', methods=['POST'])
def addTag():
    # verify that data was sent with the post request
    try:
        request
    except:
        return {
            'Ok': False,
            'ErrMsg': 'Missing post data'
        }, 200

    json = {}

    # verify that the json data sent with the post request contains a
    # tagName key
    try:
        json = request.get_json()

        if json is None or 'tagName' not in list(json.keys()):
            return {
                'Ok': False,
                'ErrMsg': 'Tag Name is missing from the request'
            }, 200
    except Exception as err:
        return json, 404

    # check to see if the tag already exists
    tagName = json['tagName']
    tag = Tag.query.filter_by(name = tagName).first()

    if tag is not None:
        return {
            'Ok': False,
            'ErrMsg': f'Tag {tagName=} already exists'
        }, 200

    ret = None
    data = {
        'name': tagName
    }

    try:
        ret = Tag(name='foobar')
        db.session.add(tag)
        db.session.commit()
    except Exception as err:
        return {
            'Ok': False,
            'ErrMsg': f'Unknown error add Tag: {err=}'
        }, 200

    return {
        'Ok': True,
        'tagId': ret.tagid
    }, 200

@tag_bp.route('<int:id>', methods=['GET'])
def getTagById():
    return {
        'Ok': False,
        'ErrMsg': 'Not Implemented'
    }, 404

@tag_bp.route('<string:tagName>', methods=['GET'])
def getTagByName():
    return {
        'Ok': False,
        'ErrMsg': 'Not Implemented'
    }, 404

@tag_bp.route('<int:id>', methods=['PUT'])
def updateTagById():
    return {
        'Ok': False,
        'ErrMsg': 'Not Implemented'
    }, 404

@tag_bp.route('<string:tagName>', methods=['PUT'])
def updateTagByName():
    return {
        'Ok': False,
        'ErrMsg': 'Not Implemented'
    }, 404

@tag_bp.route('<int:id>', methods=['DELETE'])
def deleteTagById():
    return {
        'Ok': False,
        'ErrMsg': 'Not Implemented'
    }, 404

@tag_bp.route('<string:tagName>', methods=['DELETE'])
def deleteTagByName():
    return {
        'Ok': False,
        'ErrMsg': 'Not Implemented'
    }, 404
## }}}
