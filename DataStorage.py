## © Jacob Gray 2022
## This Source Code Form is subject to the terms of the Mozilla Public
## License, v. 2.0. If a copy of the MPL was not distributed with this
## file, You can obtain one at http://mozilla.org/MPL/2.0/.

## This class is designed to store data from program for pickling

class Store():

    def __init__(self):
        self.ipAddress = ""
        self.status = -1
        self.runHour = -1
        self.succeeded = []
        self.failed = []
