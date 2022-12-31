###############################################################################
## test_shelf.py for archivist card catalog microservice unit tests          ##
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
## Unit tests for the shelf routes
##
## }}}

### test_shelf ## {{{
import pytest, json, string
from app.appfactory import create_app
from app.version import VERSION, APPNAME
from app.models.dbbase import db
from .config import TestConfig

checksum = '2ee20486d3b51eed3f850139af55c7ea'

@pytest.fixture(scope='module')
def test_client():
    app = create_app(TestConfig())

    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    client.post('/init')
    yield client

    ctx.pop()

def test_addRecord(test_client):
    """
    GIVEN a card catalog service
    WHEN POST /record is invoked
    WHEN records information is provided
    THEN the response should be 200
    THEN Ok is True
    THEN recordId is the new record number
    """
    record_data = {
        "record_type": RECORDTYPE_DOC,
        "title": "New Document",
        "filename": "NewDoc.docx",
        "checksum": checksum,
        "author": "Me",
        "userid": "1000"
    }

    resp = test_client.post('/record', json=record_data)
    assert resp.status_code == 200
    assert resp.json['Ok'] == True
    assert resp.json['recordid'].isnumeric()

## }}}
