###############################################################################
## test_status.py for archivist card catalog microservice                    ##
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
## unit tests for the status end point
##
## }}}

### test_status ## {{{

import pytest, json, string
from app.appfactory import create_app
from app.models.dbbase import db
from .config import TestConfig

@pytest.fixture(scope='module')
def test_client():
    app = create_app(TestConfig())

    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()

@pytest.fixture(scope='module')
def init_db():
    db.create_all()

    yield db

    db.drop_all()

def test_status_nodb(test_client):
    """
    GIVEN a card catalog service
    WHEN the GET /status page is requested
    WHEN the database doesn't exist
    THEN should return 200
    THEN should return that it is not connected to the database
    """

    resp = test_client.get('/status')
    assert resp.status_code == 200
    assert resp.json['database']['status'] == 'Uninitialized'

def test_status_good(test_client, init_db):
    """
    GIVEN a card catalog service
    WHEN the GET /status page is requested
    WHEN the database does exist
    THEN should return 200
    THEN should return that it is connected to the database
    THEN should return the list of tables associated with the microservice
    """

    resp = test_client.get('/status')
    assert resp.status_code == 200
    assert resp.json['database']['status'] == 'Initialized'


## }}}
