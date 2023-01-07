###############################################################################
## tags.py for archivist card catalog microservice                        ##
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
## tag model for collections
##
## }}}

### tags ## {{{
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .dbbase import db

TAGLEN = 100

class Tag(db.Model):
    __table_args__ = { "mysql_engine": "InnoDB" }
    tagid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(TAGLEN), nullable=True)

## Xref table
collectionXtag = db.Table('collectionXTab',
                          db.Column('tagid', db.Integer,
                                    db.ForeignKey('tag.tagid')),
                          db.Column('collectionid', db.Integer,
                                    db.ForeignKey('collection.collectionid')))
## }}}