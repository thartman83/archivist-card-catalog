###############################################################################
#  test_shelf.py for archivist card catalog microservice unit tests           #
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

# Commentary {{{
"""
Unit tests for the shelf routes
"""
# }}}

# test_shelf {{{
import random
import pytest
from app.appfactory import create_app
from app.models import RecordType
from app.routes.shelf import validateRecordData, required_fields
from .config import TestConfig

CHECKSUM = '2ee20486d3b51eed3f850139af55c7ea'
GOOD_RECORD_DATA = {
    "record_type": RecordType.DOCUMENT,
    "title": "New Document",
    "filename": "NewDoc.docx",
    "extension": "docx",
    "size": "101kb",
    "checksum": CHECKSUM,
    "author": "Me",
    "user": 1000
}


@pytest.fixture(scope='module', name='test_client')
def fixture_test_client():
    """
    Test client for tests
    """
    app = create_app(TestConfig())

    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    client.post('/init')
    yield client

    ctx.pop()


@pytest.fixture(scope='function', name='with_collection')
def fixture_with_collection(test_client):
    """
    Sets up a collection
    """
    resp = test_client.post('/shelf', json=GOOD_RECORD_DATA)
    collectionid = resp.json['collectionid']
    resp = test_client.get(f'/shelf/{collectionid}')

    return resp.json['collection']


#################
# Enpoint Tests #
#################
def test_add_collection(test_client):
    """
    GIVEN a card catalog service
    WHEN POST /collection is invoked
    WHEN records information is provided
    THEN the response should be 200
    THEN Ok is True
    THEN recordId is the new record number
    """
    resp = test_client.post('/shelf', json=GOOD_RECORD_DATA)
    assert resp.status_code == 200
    assert resp.json['Ok']
    assert isinstance(resp.json['collectionid'], int)


def test_read_collection(test_client, with_collection):
    """
    GIVEN a card catalog service
    WHEN GET /shelf/id is invoked
    WHEN the record id is valid
    THEN the response should be 200
    THEN Ok is True
    THEN the record information is provided
    """
    collectionid = with_collection['collectionid']
    resp = test_client.get(f'/shelf/{collectionid}')
    assert resp.status_code == 200
    assert resp.json['Ok']
    assert resp.json['collection']['collectionid'] == collectionid

    expected_data = GOOD_RECORD_DATA.copy()
    user = expected_data.pop('user', None)
    expected_data['creation_user'] = user
    keys = list(expected_data.keys())
    for key in keys:
        assert resp.json['collection']['edition'][key] == expected_data[key]

    assert resp.json['collection']['current_edition'] == 1


def test_read_collection_bad_id(test_client):
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
    assert resp.json['Ok'] is False
    assert resp.json['ErrMsg'] == 'Unknown collection 1000'


def test_add_edition(test_client, with_collection):
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
    new_title = 'New Edition'
    new_checksum = 'foobarbaz'
    new_edition_number = with_collection['current_edition'] + 1
    new_user = 2002

    new_edition = GOOD_RECORD_DATA.copy()
    new_edition['title'] = new_title
    new_edition['user'] = new_user
    new_edition['checksum'] = new_checksum
    resp = test_client.post(f'/shelf/{collectionid}', json=new_edition)
    assert resp.status_code == 200
    assert resp.json['Ok']
    assert resp.json['collection']['collectionid'] == collectionid
    assert resp.json['collection']['current_edition'] == new_edition_number
    assert resp.json['collection']['creation_user'] == 1000
    assert resp.json['collection']['modified_user'] == new_user
    assert resp.json['collection']['edition']['title'] == new_title
    assert resp.json['collection']['edition']['checksum'] == new_checksum


def test_add_edition_multiple(test_client, with_collection):
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
    edition_count = random.randint(3, 10)

    assert with_collection['current_edition'] == 1

    for i in range(2, edition_count):
        new_edition = GOOD_RECORD_DATA.copy()
        new_title = "NewDocumentEdition" + str(i)
        new_edition['title'] = new_title
        resp = test_client.post(f'/shelf/{collectionid}', json=new_edition)
        assert resp.status_code == 200
        assert resp.json['Ok']
        assert resp.json['collection']['collectionid'] == collectionid
        assert resp.json['collection']['current_edition'] == i
        assert resp.json['collection']['edition']['title'] == new_title


def test_add_edition_bad_collection(test_client):
    """
    GIVEN a card catalog service
    WHEN a collection i does not exist
    WHEN the post /shelf/{i} is invoked
    THEN the response should be 200
    THEN Ok should be False
    Then the error message should be correct
    """
    collectionid = 127
    new_edition = GOOD_RECORD_DATA.copy()
    resp = test_client.post(f'shelf/{collectionid}', json=new_edition)
    assert resp.status_code == 200
    assert resp.json['Ok'] is False
    assert resp.json['ErrMsg'] == f'Unknown collection {collectionid}'


def test_get_edition_single(test_client, with_collection):
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

    resp = test_client.get(f'/shelf/{collectionid}/edition')
    assert resp.status_code == 200
    assert resp.json['Ok']
    assert resp.json['collectionid'] == collectionid
    assert len(resp.json['editions']) == 1

    expected_data = GOOD_RECORD_DATA.copy()
    user = expected_data.pop('user', None)
    expected_data['creation_user'] = user
    keys = list(expected_data.keys())
    for key in keys:
        assert resp.json['editions'][0][key] == expected_data[key]


def test_get_edition_multiple(test_client, with_collection):
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
    edition_count = random.randint(3, 10)

    for i in range(2, edition_count):
        new_edition = GOOD_RECORD_DATA.copy()
        new_title = "NewDocumentEdition" + str(i)
        new_edition['title'] = new_title
        resp = test_client.post(f'/shelf/{collectionid}', json=new_edition)

    resp = test_client.get(f'/shelf/{collectionid}/edition')
    assert resp.status_code == 200
    assert resp.json['Ok']
    assert resp.json['collectionid'] == collectionid
    assert len(resp.json['editions']) == edition_count - 1


def test_get_edition_bad_collection(test_client):
    """
    GIVEN a card catalog service
    WHEN a collection i does not exist
    WHEN the GET /shelf/{i}/edition is invoked
    THEN the response should be 200
    THEN Ok should be False
    THEN should return the correct error message
    """
    collectionid = 2000
    resp = test_client.get(f'shelf/{collectionid}/edition')

    assert resp.status_code == 200
    assert resp.json['Ok'] is False
    assert resp.json['ErrMsg'] == 'Unknown collection 2000'


def test_get_specific_edition(test_client, with_collection):
    """
    GIVEN a card catalog service
    WHEN a collection i exists
    WHEN the collection has a single edition
    WHEN the GET /shelf/{i}/edition/{j} is invoked
    WHEN edition j exists
    THEN the status code should be 200
    THEN Ok should be True
    THen should return the edition
    """
    collectionid = with_collection['collectionid']
    editionid = with_collection['current_edition']

    resp = test_client.get(f'/shelf/{collectionid}/edition/{editionid}')

    assert resp.status_code == 200
    assert resp.json['collectionid'] == collectionid
    assert resp.json['edition']['edition'] == editionid


def test_get_specific_edition_random(test_client, with_collection):
    """
    GIVEN a card catalog service
    WHEN a collection i exists
    WHEN the collection has a single edition
    WHEN the GET /shelf/{i}/edition/{j} is invoked
    WHEN edition j exists
    THEN the status code should be 200
    THEN Ok should be True
    THen should return the edition
    """
    collectionid = with_collection['collectionid']
    edition_count = random.randint(3, 10)

    for i in range(2, edition_count):
        new_edition = GOOD_RECORD_DATA.copy()
        new_title = "NewDocumentEdition" + str(i)
        new_edition['title'] = new_title
        resp = test_client.post(f'/shelf/{collectionid}', json=new_edition)

    specific_edition = random.randint(3, 10)

    resp = test_client.get(f'/shelf/{collectionid}/edition/{specific_edition}')
    assert resp.status_code == 200
    print(resp.json)
    assert resp.json['collectionid'] == collectionid
    assert resp.json['edition']['edition'] == specific_edition


def test_get_specific_edition_bad_collection(test_client):
    """
    GIVEN a card catalog service
    WHEN a collection i does not exist
    WHEN the collection has a single edition
    WHEN the GET /shelf/{i}/edition/{j} is invoked
    THEN the status code should be 200
    THEN Ok should be False
    THen the error meessage should be correct
    """
    collectionid = 200
    editionid = 2
    resp = test_client.get(f'/shelf/{collectionid}/edition/{editionid}')

    assert resp.status_code == 200
    assert resp.json['Ok'] is False
    assert resp.json['ErrMsg'] == f"Unknown collection {collectionid}"


def test_get_specific_edition_bad_edition(test_client, with_collection):
    """
    GIVEN a card catalog service
    WHEN a collection i does exist
    WHEN the collection has editions
    WHEN the GET /shelf/{i}/edition/{j} is invoked
    WHEN edition j does not exist
    THEN the status code should be 200
    THEN Ok should be False
    THen the error meessage should be correct
    """
    collectionid = with_collection['collectionid']
    editionid = 10
    resp = test_client.get(f'/shelf/{collectionid}/edition/{editionid}')

    assert resp.status_code == 200
    assert resp.json['Ok'] is False
    assert resp.json['ErrMsg'] == f"Unknown edition {editionid}"


#####################
# Method Unit Tests #
#####################
def test_validate_record_data_good():
    """
    GIVEN
    """
    res, _ = validateRecordData(GOOD_RECORD_DATA)
    assert res


def test_validate_record_data_missing():
    """
    GIVEN
    """
    for field in required_fields:
        data = GOOD_RECORD_DATA.copy()
        data.pop(field, None)
        res, errs = validateRecordData(data)
        assert res is False
        assert errs['ErrMsg'][0] == f"Missing {field} field"


def test_validate_record_data_bad_record_type():
    """
    GIVEN
    """
    data = GOOD_RECORD_DATA.copy()
    data['record_type'] = "NAN"
    res, errs = validateRecordData(data)
    assert res is False
    print(errs)
    assert errs['ErrMsg'][0] == "record_type is not valid"


def test_validate_record_data_unknown_record_type():
    """
    GIVEN
    """
    data = GOOD_RECORD_DATA.copy()
    data['record_type'] = len(RecordType) + 1
    res, errs = validateRecordData(data)
    assert res is False
    assert errs['ErrMsg'][0] == f"Unknown record type {len(RecordType) + 1}"


def test_validate_record_data_junk():
    """
    Given
    """
    data = ""
    res, _ = validateRecordData(data)
    assert res is False

# }}}
