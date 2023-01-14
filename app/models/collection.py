###############################################################################
#  collection.py for archivist card catalog microservice                      #
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

# Commentary ## {{{
"""
ollection of editions of records
"""
# }}}

# collection{{{
from sqlalchemy.sql import func
from .dbbase import db
from .tags import collectionXtag


class Collection(db.Model):  # pylint: disable=too-few-public-methods
    """
    Collection Record ORM model
    """
    __table_args__ = {"mysql_engine": "InnoDB"}
    collectionid = db.Column(db.Integer, primary_key=True)
    current_edition = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.DateTime, server_default=func.now())
    creation_user = db.Column(db.Integer, nullable=False)
    modified_date = db.Column(db.DateTime, server_default=func.now())
    modified_user = db.Column(db.Integer, nullable=False)

    records = db.relationship('Shelf',
                              backref=db.backref('collection'),
                              lazy=True)

    tags = db.relationship('Tag', secondary=collectionXtag,
                           backref='collection')

    def serialize(self):
        """
        JSON of a collection
        """

        current_edition = next(filter(lambda r:
                                      r.edition == self.current_edition,
                                      self.records), None)
        serialize_edition = current_edition.serialize() if current_edition \
            else {}

        return {
            "collectionid": self.collectionid,
            "current_edition": self.current_edition,
            "creation_date": self.creation_date,
            "creation_user": self.creation_user,
            "modified_date": self.modified_date,
            "modified_user": self.modified_user,
            "edition": serialize_edition
        }
# }}}
