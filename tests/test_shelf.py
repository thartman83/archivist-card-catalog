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
import pytest, json, string, random
from app.appfactory import create_app
from app.version import VERSION, APPNAME
from app.models import db, RecordType
from .config import TestConfig
from app.routes.shelf import validateRecordData, required_fields

checksum = '2ee20486d3b51eed3f850139af55c7ea'
goodRecordData = {
    "record_type": RecordType.DOCUMENT,
    "title": "New Document",
    "filename": "NewDoc.docx",
    "extension": "docx",
    "size": "101kb",
    "checksum": checksum,
    "author": "Me",
    "user": 1000
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

@pytest.fixture(scope='function')
def with_collection(test_client):
    resp = test_client.post('/shelf', json=goodRecordData)
    collectionid = resp.json['collectionid']
    resp = test_client.get('/shelf/{0}'.format(collectionid))

    return resp.json['collection']


#######################
#### Enpoint Tests ####
#######################
def test_addCollection(test_client):
    """
    GIVEN a card catalog service
    WHEN POST /collection is invoked
    WHEN records information is provided
    THEN the response should be 200
    THEN Ok is True
    THEN recordId is the new record number
    """
    resp = test_client.post('/shelf', json=goodRecordData)
    assert resp.status_code == 200
    assert resp.json['Ok'] == True
    assert isinstance(resp.json['collectionid'],int)

def test_readCollection(test_client, with_collection):
    """
    GIVEN a card catalog service
    WHEN GET /shelf/id is invoked
    WHEN the record id is valid
    THEN the response should be 200
    THEN Ok is True
    THEN the record information is provided
    """
    collectionid = with_collection['collectionid']
    resp = test_client.get('/shelf/{0}'.format(collectionid))
    assert resp.status_code == 200
    assert resp.json['Ok'] == True
    assert resp.json['collection']['collectionid'] == collectionid

    expectedData = goodRecordData.copy()
    user = expectedData.pop('user', None)
    expectedData['creation_user'] = user
    keys = list(expectedData.keys())
    for key in keys:
        assert resp.json['collection']['edition'][key] == expectedData[key]

    assert resp.json['collection']['current_edition'] == 1

def test_readCollectionBadId(test_client):
    """
    GIVEN a card catalog service
    WHEN GET /shelf/id is invoked
    WHEN the record id is not valid
    THEN the response should be 200
    THEN Ok should be False
    THEN error message should be correct
    """

    resp = test_client.get('/shelf/1000')
    assert resp.status_code == 200
    assert resp.json['Ok'] == False
    assert resp.json['ErrMsg'] == 'Unknown collection 1000'

def test_addEdition(test_client, with_collection):
    """
    GIVEN a card catalog service
    WHEN a collection i exists
    WHEN the POST /shelf/{i} is invoked
    WHEN the post data is valid
    THEN the response should be 200
    THEN Ok should be True
    THEN should contain the updated collection
    """
    collectionid = with_collection['collectionid']
    newTitle = 'New Edition'
    newChecksum = 'foobarbaz'
    newEditionNumber = with_collection['current_edition'] + 1
    newUser = 2002

    newEdition = goodRecordData.copy()
    newEdition['title'] = newTitle
    newEdition['user'] = newUser
    newEdition['checksum'] = newChecksum
    resp = test_client.post('/shelf/{0}'.format(collectionid), json=newEdition)
    assert resp.status_code == 200
    assert resp.json['Ok'] == True
    assert resp.json['collection']['collectionid'] == collectionid
    assert resp.json['collection']['current_edition'] == newEditionNumber
    assert resp.json['collection']['creation_user'] == 1000
    assert resp.json['collection']['modified_user'] == newUser
    assert resp.json['collection']['edition']['title'] == newTitle
    assert resp.json['collection']['edition']['checksum'] == newChecksum

def test_addEditionMultiple(test_client, with_collection):
    """
    GIVEN a card catalog service
    WHEN a collection i exists
    WHEN the POST /shelf/{i} n times
    WHEN the post data is valid for n times
    THEN the response should be 200 for n times
    THEN Ok should be True for n times
    THEN should contain the updated collection
    THEN should should have n as current version
    """
    collectionid = with_collection['collectionid']

    # generate a random number of new editions
    editionCount = random.randint(3,10)

    assert with_collection['current_edition'] == 1

    for i in range(2, editionCount):
        newEdition = goodRecordData.copy()
        newTitle = "NewDocumentEdition" + str(i)
        newEdition['title'] = newTitle
        resp = test_client.post('/shelf/{0}'.format(collectionid), json=newEdition)
        assert resp.status_code == 200
        assert resp.json['Ok'] == True
        assert resp.json['collection']['collectionid'] == collectionid
        assert resp.json['collection']['current_edition'] == i
        assert resp.json['collection']['edition']['title'] == newTitle

def test_addEditionBadCollection(test_client):
    """
    GIVEN a card catalog service
    WHEN a collection i does not exist
    WHEN the post /shelf/{i} is invoked
    THEN the response should be 200
    THEN Ok should be False
    Then the error message should be correct
    """
    collectionid = 127
    newEdition = goodRecordData.copy()
    resp = test_client.post('shelf/{0}'.format(collectionid), json=newEdition)
    assert resp.status_code == 200
    assert resp.json['Ok'] == False
    assert resp.json['ErrMsg'] == 'Unknown collection {0}'.format(collectionid)

def test_getEditionSingle(test_client, with_collection):
    """
    GIVEN a card catalog service
    WHEN a collection i does exist
    WHEN the collection has 1 edition
    WHEN the GET /shelf/{i}/edition is invoked
    THEN the response should be 200
    THEN Ok should be True
    THEN should return an array of a single edition
    """
    collectionid = with_collection['collectionid']

    resp = test_client.get('/shelf/{0}/edition'.format(collectionid))
    assert resp.status_code == 200
    assert resp.json['Ok'] == True
    assert resp.json['collectionid'] == collectionid
    assert len(resp.json['editions']) == 1

    expectedData = goodRecordData.copy()
    user = expectedData.pop('user', None)
    expectedData['creation_user'] = user
    keys = list(expectedData.keys())
    for key in keys:
        assert resp.json['editions'][0][key] == expectedData[key]

def test_getEditionMultiple(test_client, with_collection):
    """
    GIVEN a card catalog service
    WHEN a collection i does exist
    WHEN the collection has n editions
    WHEN the GET /shelf/{i}/edition is invoked
    THEN the response should be 200
    THEN Ok should be True
    THEN should return an array of n editions
    """
    collectionid = with_collection['collectionid']
    editionCount = random.randint(3,10)

    for i in range(2, editionCount):
        newEdition = goodRecordData.copy()
        newTitle = "NewDocumentEdition" + str(i)
        newEdition['title'] = newTitle
        resp = test_client.post('/shelf/{0}'.format(collectionid), json=newEdition)

    resp = test_client.get('/shelf/{0}/edition'.format(collectionid))
    assert resp.status_code == 200
    assert resp.json['Ok'] == True
    assert resp.json['collectionid'] == collectionid
    assert len(resp.json['editions']) == editionCount - 1

def test_getEditionBadCollection(test_client):
    """
    GIVEN a card catalog service
    WHEN a collection i does not exist
    WHEN the GET /shelf/{i}/edition is invoked
    THEN the response should be 200
    THEN Ok should be False
    THEN should return the correct error message
    """
    collectionid = 2000
    resp = test_client.get('shelf/{0}/edition'.format(collectionid))

    assert resp.status_code == 200
    assert resp.json['Ok'] == False
    assert resp.json['ErrMsg'] == 'Unknown collection 2000'

###########################
#### Method Unit Tests ####
###########################
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
