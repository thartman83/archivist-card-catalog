###############################################################################
## test_tag.py for archivist card catalog microservice                        ##
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
## tag tests
##
## }}}

### test_tag ## {{{

import pytest, json, string
from app.appfactory import create_app
from app.models import tags
from .config import TestConfig

aTagName = 'ANewTag'
aTagData = {
    'tagName': aTagName
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
def with_tag(test_client):
    resp = test_client.post('/tag', json=aTagData)
    return resp.json

###################
#### Tag Tests ####
###################
def test_addTag(test_client):
    """
    GIVEN a card catalog microserve
    WHEN POST /tag is invoked
    WHEN tagname is passed to the endpoint
    THEN the response should be 200
    THEN Ok should be True
    THEN tagid should be the new tag id
    """
    resp = test_client.post('/tag', json=aTagData)
    print(resp.json)
    assert resp.status_code == 200
    assert resp.json['Ok'] == True
    assert resp.json.has_key('tagId') == True

def test_addTagAlreadyExists(test_client, with_tag):
    """
    GIVEN a card catalog microserve
    WHEN POST /tag is invoked
    WHEN tagname is passed to the endpoint
    WHEN the tag already exists
    THEN the response should be 200
    THEN Ok should be False
    THEN ErrMsg should be correct
    """
    resp = test_client.post('/tag', json=aTagData)
    tagName = aTagData['tagName']
    assert resp.status_code == 200
    assert resp.json['Ok'] == False
    assert resp.json['ErrMsg'] == f"Tag {tagName=} already exists"

def test_addTagTagNameMissing(test_client):
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
    print(resp)
    assert resp.status_code == 200
    assert resp.json['Ok'] == False
    assert resp.json['ErrMsg'] == "Tag Name is missing from the request"
## }}}
