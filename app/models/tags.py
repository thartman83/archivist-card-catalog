###############################################################################
#  tags.py for archivist card catalog microservice                            #
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
tag model for collections
"""
# }}}

# tags {{{
from .dbbase import db

TAGLEN = 100


class Tag(db.Model):  # pylint: disable=too-few-public-methods
    """
    Tag ORM
    """
    __table_args__ = {"mysql_engine": "InnoDB"}
    tagid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(TAGLEN), nullable=False)

    def serialize(self):
        """
        Return a dictionary version of the Tag model
        """
        return {
            "tagid": self.tagid,
            "name": self.name
        }


collectionXtag = db.Table('collectionXTag',
                          db.Column('tagid', db.Integer,
                                    db.ForeignKey('tag.tagid')),
                          db.Column('collectionid', db.Integer,
                                    db.ForeignKey('collection.collectionid')))
# }}}
