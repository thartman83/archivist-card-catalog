###############################################################################
## shelf.py for archivist card catalog microservice models                 ##
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
## shelf model
##
## }}}

### shelf ## {{{
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from .dbbase import db
from datetime import datetime
from enum import IntEnum

class Shelf(db.Model):
    __table_args__ = { "mysql_engine": "InnoDB" }
    id = db.Column(db.Integer, primary_key=True)

class RecordType(IntEnum):
    DOCUMENT = 1
    EMAIL = 2

## }}}
