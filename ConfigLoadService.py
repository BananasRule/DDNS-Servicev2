import logging


## Service for loading the DNS config file
# Uses file called dnsconfig.conf
# @returns A dictionary containing setting fields (raw from file) and zone information
def DNSConfigLoad():
    # Parse config files
    dnsConfig = open("dnsconfig.conf")
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
                    dnsSettings["zones"].append(["", "", "", False, []])
                elif setting == "!ENDDNSZONE":
                    # Check zone meets minimum requirements
                    if dnsSettings["zones"][currentZoneNum][0] != "" and dnsSettings["zones"][currentZoneNum][1] != "" \
                       and dnsSettings["zones"][currentZoneNum][2] != "":
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
                if value[0] == "$":
                    if value in variables:
                        value = variables[value]

                match var:
                    case "zoneName":
                        dnsSettings["zones"][currentZoneNum][0] = value
                    case "zoneID":
                        dnsSettings["zones"][currentZoneNum][1] = value
                    case "zoneKey":
                        dnsSettings["zones"][currentZoneNum][2] = value
                    case "listType":
                        if value.upper() == "DENY":
                            dnsSettings["zones"][currentZoneNum][3] = False
                        elif value.upper() == "ALLOW":
                            dnsSettings["zones"][currentZoneNum][3] = True
                        else:
                            logging.warning("Error setting list type, defaulting to deny list")
                            dnsSettings["zones"][currentZoneNum][3] = False
                    case "list":
                        dnsSettings["zones"][currentZoneNum][4] = value.split(",")
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
    return dnsSettings


## Service for loading the mail config file
# Uses file called mailconfig.conf
# @returns A dictionary containing setting fields (raw from file) and zone information
def MailConfigLoad():

    mailConfig = open("mailconfig.conf")
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
                # Store in dictonary
                mailSettings[var] = value

    return mailSettings


