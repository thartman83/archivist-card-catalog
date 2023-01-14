###############################################################################
#  shelf.py for archivist card catalog microservice models                    #
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
## shelf model
"""
# }}}

# shelf {{{
from enum import IntEnum
from sqlalchemy.sql import func
from .dbbase import db


class Shelf(db.Model):  # pylint: disable=too-few-public-methods
    """
    Shelf ORM
    """
    __table_args__ = {"mysql_engine": "InnoDB"}
    recordid = db.Column(db.Integer, primary_key=True)
    collectionid = db.Column(db.Integer,
                             db.ForeignKey('collection.collectionid'))
    edition = db.Column(db.Integer, nullable=False)
    record_type = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    extension = db.Column(db.String(10), nullable=False)
    size = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    checksum = db.Column(db.String(64), nullable=False)
    creation_date = db.Column(db.DateTime, server_default=func.now())
    creation_user = db.Column(db.Integer, nullable=False)

    def serialize(self):
        """
        Return the Shelf record as a dictionary
        """
        return {
            "recordid": self.recordid,
            "collectionid": self.collectionid,
            "edition": self.edition,
            "record_type": self.record_type,
            "title": self.title,
            "filename": self.filename,
            "extension": self.extension,
            "size": self.size,
            "author": self.author,
            "checksum": self.checksum,
            "creation_date": self.creation_date,
            "creation_user": self.creation_user,
        }


class RecordType(IntEnum):  # pylint: disable=too-few-public-methods
    """
    Record Type enum
    """
    DOCUMENT = 1
    EMAIL = 2

# }}}
