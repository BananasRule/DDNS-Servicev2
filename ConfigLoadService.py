import logging

# A class used to store zone information
class zone:
    def __init__(self):
        self.name = ""
        self.ID = ""
        self.apiKey = ""
        self.listType = True
        self.list = []

## Service for loading the DNS config file
# Uses file called dnsconfig.conf in config directory (config/dnsconfig.conf)
# @returns A dictionary containing setting fields (raw from file) and zone information
def DNSConfigLoad():
    # Parse config files
    dnsConfig = open("config/dnsconfig.conf")
    dnsSettings = {}
    dnsSettings["zones"] = []
    variables = {}
    inDnsZone = False
    currentZoneNum = 0

    for line in dnsConfig:
        # Remove any whitespace
        line = line.replace(" ", "")
        # Remove line endings
        line = line.replace("\n", "")
        # Remove comment from line, supporting inline comments
        setting = line.split("#")[0]
        # Check that line contains a setting and not just comment or whitespace
        if len(setting) != 0:
            # Store variables defined
            if setting[0] == "$":
                var, value = setting.split("=", 1)
                # Store in dictonary
                variables[var] = value
            elif setting[0] == "!":
                if setting == "!BEGINDNSZONE":
                    inDnsZone = True
                    # Add new zone with default values
                    dnsSettings["zones"].append(zone())
                elif setting == "!ENDDNSZONE":
                    # Check zone meets minimum requirements
                    if dnsSettings["zones"][currentZoneNum].name != "" and dnsSettings["zones"][currentZoneNum].id != "" \
                       and dnsSettings["zones"][currentZoneNum].apiKey != "":
                        # Get next index
                        currentZoneNum = currentZoneNum + 1
                        inDnsZone = False
                    else:
                        logging.error("Error getting zone details, removing zone and attempting to recover")
                        dnsSettings["zones"].pop()
                        inDnsZone = False
            elif inDnsZone:
                var, value = setting.split("=", 1)

                # Check if value is a variable and is in variables dictionary
                # If it is not treat as a literal
                if len(value) != 0:
                    if value[0] == "$":
                        if value in variables:
                            value = variables[value]

                    match var:
                        case "zoneName":
                            dnsSettings["zones"][currentZoneNum].name = value
                        case "zoneID":
                            dnsSettings["zones"][currentZoneNum].id = value
                        case "zoneKey":
                            dnsSettings["zones"][currentZoneNum].apiKey = value
                        case "listType":
                            if value.upper() == "DENY":
                                dnsSettings["zones"][currentZoneNum].listType = True
                            elif value.upper() == "ALLOW":
                                dnsSettings["zones"][currentZoneNum].listType = False
                            else:
                                logging.warning("Error setting list type, defaulting to deny list")
                                dnsSettings["zones"][currentZoneNum].listType = True
                        case "list":
                            dnsSettings["zones"][currentZoneNum].list = value.split(",")
            else:
                # Not part of zone
                # Split setting into name and variable
                var, value = setting.split("=", 1)
                # Check if value is a variable and is in variables dictionary
                # If it is not treat as a literal
                if value[0] == "$":
                    if value in variables:
                        value = variables[value]
                # Store in dictonary
                dnsSettings[var] = value
    dnsConfig.close()
    return dnsSettings


## Service for loading the mail config file
# Uses file called mailconfig.conf in config directory (config/mailconfig.conf)
# @returns A dictionary containing setting fields (raw from file) and zone information
def MailConfigLoad():

    mailConfig = open("config/mailconfig.conf")
    mailSettings = {}
    variables = {}
    for line in mailConfig:
        # Remove any whitespace
        line = line.replace(" ", "")
        # Remove line endings
        line = line.replace("\n", "")
        # Remove comment from line, supporting inline comments
        setting = line.split("#")[0]
        # Check that line contains a setting and not just comment or whitespace
        if len(setting) != 0:
            if setting[0] == "$":
                var, value = setting.split("=", 1)
                # Store in dictonary
                variables[var] = value
            else:
                # Split setting into name and variable
                var, value = setting.split("=", 1)
                # Check if value is a variable and is in variables dictionary
                # If it is not treat as a literal
                if value[0] == "$":
                    if value in variables:
                        value = variables[value]
                # Store in dictionary
                mailSettings[var] = value
    mailConfig.close()
    return mailSettings


