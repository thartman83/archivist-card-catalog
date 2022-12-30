###############################################################################
## run.py for archivist card catalog microservices                           ##
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
## Main entry point for the flask microservice
##
## }}}

### run ## {{{
import os
from app import create_app, Config

if __name__ == "__main__":
    cfg = Config()

    # ingest the run time options from env variables
    cfg.dbEngine = os.environ.get('DBEngine')
    cfg.dbHost = os.environ.get('DBHost')
    cfg.dbName = os.environ.get('DBName')
    cfg.dbUser = os.environ.get('DBUser')
    cfg.dbPasswd = os.environ.get('DBPasswd')
    cfg.storageLocation = os.environ.get('StorageLocation')

    app = create_app(cfg)
    app.run()

## }}}
