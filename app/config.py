###############################################################################
## config.py for archivist card catalog microservice                        ##
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
## configuration information for the archivist card catalog microservice
##
## }}}

### config ## {{{
class AppConfig:
    DEBUG = True
    TESTING = True
    ENVIRONMENT = "DEV"
    SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODFICITIONS=False

class DevConfig(AppConfig):
    DEBUG = True
    TESTING = True
    ENVIRONMENT = "DEV"
    SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODFICITIONS=False

Configs = {
    "DEV": DevConfig
}

## }}}
