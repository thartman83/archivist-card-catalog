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
    recordid = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    extension = db.Column(db.String(10), nullable=False)
    size = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    checksum = db.Column(db.String(64), nullable=False)
    current_version = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime, server_default=func.now())
    creation_user = db.Column(db.Integer, nullable=False)
    modified_date = db.Column(db.DateTime, server_default=func.now())
    modified_user = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "recordid": self.recordid,
            "record_type": self.recordtype,
            "title": self.title,
            "filename": self.filename,
            "extension": self.extension,
            "size": self.size,
            "author": self.author,
            "checksum": self.checksum,
            "current_version": self.current_version,
            "creation_date": self.creation_date,
            "creation_user": self.creation_user,
            "modified_date": self.modified_date,
            "modified_user": self.modified_user
        }

class RecordType(IntEnum):
    DOCUMENT = 1
    EMAIL = 2

## }}}
