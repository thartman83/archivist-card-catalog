###############################################################################
#  test_tag.py for archivist card catalog microservice                        #
#  Copyright (c) 2023 Tom Hartman (thomas.lees.hartman@gmail.com)             #
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
tag unit tests
"""
# }}}

# test_tag {{{

import pytest
from app.appfactory import create_app
from .config import TestConfig

A_TAG_NAME = 'ANewTag'
A_TAG_DATA = {
    'tagName': A_TAG_NAME
}


@pytest.fixture(scope='module', name='test_client')
def fixture_test_client():
    """
    Test client fixture used by unit tests
    """
    app = create_app(TestConfig())

    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    client.post('/init')
    yield client

    ctx.pop()


@pytest.fixture(scope='function', name='with_tag')
def fixture_with_tag(test_client):
    """
    Testing fixture that for a specific tag
    """
    resp = test_client.post('/tag', json=A_TAG_DATA)
    return resp.json


###################
#    Tag Tests    #
###################
def test_add_tag(test_client):
    """
    GIVEN a card catalog microserve
    WHEN POST /tag is invoked
    WHEN tagname is passed to the endpoint
    THEN the response should be 200
    THEN Ok should be True
    THEN tagid should be the new tag id
    """
    resp = test_client.post('/tag', json=A_TAG_DATA)
    print(resp.json)
    assert resp.status_code == 200
    assert resp.json['Ok']
    assert resp.json.has_key('tagId')


def test_add_tag_already_exists(test_client, with_tag):
    """
    GIVEN a card catalog microserve
    WHEN POST /tag is invoked
    WHEN tagname is passed to the endpoint
    WHEN the tag already exists
    THEN the response should be 200
    THEN Ok should be False
    THEN ErrMsg should be correct
    """
    resp = test_client.post('/tag', json=A_TAG_DATA)
    tag_name = A_TAG_DATA['tagName']
    assert with_tag
    assert resp.status_code == 200
    assert resp.json['Ok'] is False
    assert resp.json['ErrMsg'] == f"Tag {tag_name} already exists"


def test_add_tag_tag_name_missing(test_client):
    """
    GIVEN a card catalog microserve
    WHEN POST /tag is invoked
    WHEN tagname is passed to the endpoint
    WHEN the tag name is missing
    THEN the response should be 200
    THEN Ok should be False
    THEN ErrMsg should be correct
    """
    resp = test_client.post('/tag', json={})
    assert resp.status_code == 200
    assert resp.json['Ok'] is False
    assert resp.json['ErrMsg'] == "Tag Name is missing from the request"
# }}}
