## © Jacob Gray 2022
## This Source Code Form is subject to the terms of the Mozilla Public
## License, v. 2.0. If a copy of the MPL was not distributed with this
## file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests, time, logging
# Requests
# Copyright 2019 Kenneth Reitz

## Gets IP address from web based services
# @param IPv4 Get IPv4 address (Bool)
# @throws getIPError Cannot connect to IP server
# @returns Current IP Address (String)

def Get(IPv4 = True):

    # Get logger from main process 
    logger = logging.getLogger(__name__)

    # Variables to determine services to use
    if IPv4 == True:
        primaryServer = "https://ip4.seeip.org"
        fallbackServer = "https://api.ipify.org/"
    else:
        primaryServer = "https://ip6.seeip.org"
        # Ipify will not guarantee a ipv6 address returns
        # Hence only seeip is used
        # If there are better server please raise an issue in github
        fallbackServer = "https://ip6.seeip.org"

    try:
        # Attempt to get IP address from primary server
        ipAddressResponse = requests.get(primaryServer)
        # Check that a valid response was received 
        if ipAddressResponse.status_code != 200:
            raise getIPError()

    # This is a broad except as any error caught should cause the fallback server to be used
    # in an attempt to recover
    except:
        # Log error
        logger.warning("An unexpected error occurred with the primary IP service. Attempting connection to fallback server.")
        # Wait to mitigate unexpected short network interruptions
        time.sleep(30)
        ipAddressResponse = requests.get(fallbackServer)
        if ipAddressResponse.status_code != 200:
            raise getIPError()

    return ipAddressResponse.text



class getIPError(Exception):
    pass

