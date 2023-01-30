## © Jacob Gray 2022
## This Source Code Form is subject to the terms of the Mozilla Public
## License, v. 2.0. If a copy of the MPL was not distributed with this
## file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests, time
# Requests
# Copyright 2019 Kenneth Reitz

## Gets IP address from web based services
# @throws getIPError Cannot connect to IP server
# @returns Current IP Address (String)

def Get(IPv4 = True):

    # Variables to determine services to use
    if IPv4 == True:
        primaryServer = "https://ip4.seeip.org"
        fallbackServer = "https://api.ipify.org/"
    else:
        primaryServer = "https://ip6.seeip.org"
        fallbackServer = "https://api64.ipify.org"

    try:
        # Attempt to get IP address from primary server
        ipAddressResponce = requests.get(primaryServer)
        # Check that a valid responce was
        if ipAddressResponce.status_code != 200:
            raise getIPError()

    # This is a broad except as any error caught should cause the fallback server to be used
    # in an attempt to recover
    except:
        # Wait to mitgate unexpected short network interuptions
        time.sleep(30)
        ipAddressResponce = requests.get(fallbackServer)
        if ipAddressResponce.status_code != 200:
            raise getIPError()

    return ipAddressResponce.text



class getIPError(Exception):
    pass

