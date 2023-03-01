## © Jacob Gray 2022
## This Source Code Form is subject to the terms of the Mozilla Public
## License, v. 2.0. If a copy of the MPL was not distributed with this
## file, You can obtain one at http://mozilla.org/MPL/2.0/.


import requests, logging
# Requests
# Copyright 2019 Kenneth Reitz

class AccessService:

    ## Initialise the object
    # @param authToken Cloudflare API key with zone edit permissions
    # @param zoneURL The zone id of the target zone
    def __init__(self, authToken, zoneURL):
        # Define cloudflare secret credentials for object
        self.authToken = authToken
        self.zoneURL = zoneURL


    ## Get all IPv4 / A records
    # Return relevant details about each record needed for updating
    # @param IPv4 IPv4 records vs IPv6 (Bool) (Default = True)
    # @returns 2D Array containing domains and their ID, name and listed ip address
    # @throws AccessError Exception is thrown when function is unable to access records
    def GetAllRecords(self, IPv4 = True):
        # Get logger from main process 
        logger = logging.getLogger(__name__)

        # Define request headers
        if IPv4:
            parameters = {"type": "A"}
        else:
            parameters = {"type":"AAAA"}
        headers = {"Authorization":"Bearer " + self.authToken,"Content-Type":"application/json"}
        # Catch errors relating to getting or sorting the record
        try:
            #Send request
            listOfRecords = requests.get("https://api.cloudflare.com/client/v4/zones/" + self.zoneURL + "/dns_records", headers=headers, params=parameters)
            #Convert request from json and separate to wanted array
            listOfRecords = listOfRecords.json()
            listOfRecords = listOfRecords["result"]
            recordDetails = []
            #Loop through results array and pull wanted info into a 2D array
            for item in listOfRecords:
                domainID = item["id"]
                domainName = item["name"]
                ipAddress = item["content"]
                domainTTL = item["ttl"]
                domainProxied = item["proxied"]
                recordDetails.append([domainID, domainName, ipAddress, domainTTL, domainProxied])
            return recordDetails
        except:
            #In the event of a error throw
            logger.error("Unable to access records from cloudflare. There may be a configuration issue")
            raise AccessError("Unable to access records from cloudflare. There may be a configuration issue")

    ## Update DNS records
    # Update DNS records when old IP address exists and DNS name does not match list
    # @param ipAddress Current ip address
    # @param list Domains for blacklist / whitelist
    # @param blacklist Is the list a blacklist or whitelist (default:true)
    # @param IPv4 Is IPv4 address (vs IPv6) (default = True)
    # @returns 2D array [Success Domains[], Failed Domains[], Blocked by list[]]
    # @throws ModifyError Exception is thrown when a error occurs whilst Modifying records
    # @throws AccessError Originates from getAllRecords; Exception is thrown when function is unable to access records
    def UpdateRecords(self, ipAddress, list = [], denylist = True, IPv4 = True):
        # Get logger from main process 
        logger = logging.getLogger(__name__)
        # See output above
        status = [[],[],[]]
        # Get list of records from server
        # Needs refactoring to catch errors generated
        records = self.GetAllRecords()
        # Iterate over each record
        try:
            for record in records:
                # Check that record is not blacklisted or is included in whitelist (depending on selection)
                if (((not (record[1] in list)) and denylist == True) or ((record[1] in list) and denylist == False)):
                    #Check that record ip address does not equal current ip address
                    if record[2] != ipAddress:
                        try:
                            #Content for request
                            #Set type based on IPv4 or 6
                            if IPv4 == True:
                                content = {
                                "type": "A",
                                "name": str(record[1]),
                                "content" : str(ipAddress),
                                "ttl": str(record[3]),
                                "proxied" : record[4]
                                }
                            else:
                                content = {
                                "type": "AAAA",
                                "name": str(record[1]),
                                "content" : str(ipAddress),
                                "ttl": str(record[3]),
                                "proxied" : record[4]
                                }

                            headers = {
                                "Authorization": ("Bearer " + self.authToken),
                                "content-type": "application/json"
                            }

                            #Send request
                            changeResponse = requests.put(("https://api.cloudflare.com/client/v4/zones/" + self.zoneURL + "/dns_records/" + record[0]), headers=headers, json=content)
                            changeResponse = changeResponse.json()

                            #Handle incorrect responses
                            if changeResponse["success"] == True:
                                status[0].append(record[1])
                            else:
                                status[1].append(record[1])
                        except:
                            status[1].append(record[1])
                else:
                    status[2].append(record[1])
        except:
            logger.error("An error occurred when attempting to modify DNS records. There may be a configuration error")
            raise ModifyError("An error occurred when attempting to modify DNS records. There may be a configuration error")
        return status

#Define exceptions
class AccessError(Exception):
    pass

class ModifyError(Exception):
    pass










