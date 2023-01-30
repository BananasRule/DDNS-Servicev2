## © Jacob Gray 2022
## This Source Code Form is subject to the terms of the Mozilla Public
## License, v. 2.0. If a copy of the MPL was not distributed with this
## file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This class is designed to send messages to the user via email

import smtplib, datetime

class Messenger:

    ## Initalise object
    # @param server Server web address (String)
    # @param port Server STMP port (Int)
    # @param key API Key / Username (String)
    # @param secret API Secret / Password (String)
    # @param TLS Use TLS (Bool)
    # @param SSL Use SSL (Bool)
    # @param sendAddress The address the message will be sent from (String)
    # @param recAddress The address the message will be sent to (String)
    def __init__(self, server, port, key, secret, tls, ssl, fromAddress, toAddress):
        self.partHeader = "To:"+ toAddress + "\nFrom:" + fromAddress + "\n"
        self.server = server
        self.port = port
        self.key = key
        self.secret = secret
        self.tls = tls
        self.ssl = ssl


    def Send(self, subject, message):
        pass

    ## Compose message to send
    # @param successUpdate A 2D array containing [[Zone Name, ID]] of successfully updated zones (2D Array)
    # @param failedUpdate A 2D array containing [[Zone Name, ID]] of zones that failed to update (2D Array)
    # @param currentIP Servers current IP address (String)
    # @param sendIP Should the current IP be included in the message (Bool)
    # @returns Message to be passed to Send module
    def Compose(successUpdate, failedUpdate, currentIP, sendIP):
        message = ""

        #Check to see if there were any failures to determine email subject
        if len(failedUpdate) == 0:
            message = message + "Subject:DNS Records Sucessfully Updated/n"
        else:
            message = message + "Subject:DNS Records Failed To Update/n"

        #Loop through each successful update message if at least one exists
        if len(successUpdate) != 0:
            #Add header message
            message = message + "The following domains sucessfully updated:\n"
            #Loop through zones listing zone and IDs
            for zone in successUpdate:
                # Shouldn't occour but to catch a blank zone anyway
                if len(zone) != 0:
                    message = message + "   " + zone[0] + "\n"
                    for id in zone[1:]:
                        message = message + "       " + id + "\n"

        #Loop through each failed update message if at least one exists
        if len(failedUpdate) != 0:
            #Add header message
            message = message + "The following domains failed to update:\n"
            #Loop through zones listing zone and IDs
            for zone in failedUpdate:
                # Shouldn't occour but to catch a blank zone anyway
                if len(zone) != 0:
                    message = message + "   " + zone[0] + "\n"
                    for id in zone[1:]:
                        message = message + "       " + id + "\n"

        #If sendIP address is true send the current IP address
        if sendIP:
            message = message + "The servers current IP address is: " + currentIP + " .\n"

        #Append date and time to message
        message = message + "This message was sent on " + datetime.now.stftime("%d/%m/%Y %H:%M:%S") + "."

        #Return message
        return message

    ## A calass function for directrly composing the message in special circumstances
    # @param subject Message subject
    # @param body Message Body
    # @returns Message to be passed to send
    def ComposeSpecial(subject, body):
        message = "Subject:" + subject + "\n" + body + "\n" + "This message was sent on " + datetime.now.stftime("%d/%m/%Y %H:%M:%S") + "."
        return message








