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
from app.models import db, RecordType
from .config import TestConfig
from app.routes.record import validateRecordData, required_fields

checksum = '2ee20486d3b51eed3f850139af55c7ea'
goodRecordData = {
    "record_type": RecordType.DOCUMENT,
    "title": "New Document",
    "filename": "NewDoc.docx",
    "extension": "docx",
    "size": "101kb",
    "checksum": checksum,
    "author": "Me",
    "user": "1000"
}


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
    resp = test_client.post('/record', json=goodRecordData)
    assert resp.status_code == 200
    print(resp.json)
    assert resp.json['Ok'] == True
    assert isinstance(resp.json['recordid'],int)

def test_validateRecordDataGood():
    res, errs = validateRecordData(goodRecordData)
    assert res == True

def test_validateRecordDataMissing():
    for field in required_fields:
        data = goodRecordData.copy()
        data.pop(field, None)
        res, errs = validateRecordData(data)
        assert res == False
        assert errs['ErrMsg'][0] == "Missing {0} field".format(field)

def test_validateRecordDataBadRecordType():
    data = goodRecordData.copy()
    data['record_type'] = "NAN"
    res, errs = validateRecordData(data)
    assert res == False
    print(errs)
    assert errs['ErrMsg'][0] == "record_type is not valid"

def test_validateRecordDataUnknownRecordType():
    data = goodRecordData.copy()
    data['record_type'] = len(RecordType) + 1
    res, errs = validateRecordData(data)
    assert res == False
    assert errs['ErrMsg'][0] == "Unknown record type {0}".format(len(RecordType) + 1)

def test_validateRecordDataJunk():
    data = ""
    res, errs = validateRecordData(data)
    assert res == False

## }}}
