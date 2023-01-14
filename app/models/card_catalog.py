###############################################################################
#  card_catalog.py for archivist card catalog microservice                    #
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

# Commentary{{{
"""
Card Catalog ORM model
"""
# }}}

# card_catalog ## {{{
from sqlalchemy.sql import func
from .dbbase import db


class CardCatalog(db.Model):  # pylint: disable=too-few-public-methods
    """
    Card Catalog Model
    """
    __table_args__ = {"mysql_engine": "InnoDB"}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(25), nullable=False)
    install_date = db.Column(db.DateTime, server_default=func.now())

    def serialize(self):
        """
        Return the card catalog information as a json object
        """
        return {
            "applicationName": self.name,
            "version": self.version,
            "installDate": self.install_date
        }

# }}}
