## © Jacob Gray 2022
## This Source Code Form is subject to the terms of the Mozilla Public
## License, v. 2.0. If a copy of the MPL was not distributed with this
## file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This class is designed to send messages to the user via email

import smtplib, datetime

class Messenger:

    ## Initialise object
    # @param server Server web address (String)
    # @param port Server SMTP port (Int)
    # @param key API Key / Username (String)
    # @param secret API Secret / Password (String)
    # @param tls Use TLS (Bool)
    # @param ssl Use SSL (Bool)
    # @param fromAddress The address the message will be sent from (String)
    # @param toAddress The address the message will be sent to (String)
    def __init__(self, server, port, key, secret, tls, ssl, fromAddress, toAddress):
        self.partHeader = "To:"+ toAddress + "\nFrom:" + fromAddress + "\n"
        self.server = server
        self.port = port
        self.key = key
        self.secret = secret
        self.tls = tls
        self.ssl = ssl
        self.fromAddress = fromAddress
        self.toAddress = toAddress

    ## Function used to send messages
    # @param subject The message subject
    # @param message The message to send
    def Send(self, subject, message):
        # Create header and message to send
        header = self.partHeader + "Subject:" + subject + "\n"
        msg = header + message

        # Connect to server
        if self.ssl:
            mailServer = smtplib.SMTP_SSL(self.server, self.port)
        else:
            mailServer = smtplib.SMTP(self.server, self.port)

        # If TLS is enabled and SSL is not
        if self.tls and not self.ssl:
            mailServer.starttls()
            mailServer.ehlo()

        # Login to mail server
        mailServer.login(self.key, self.secret)

        # Send message
        mailServer.sendmail(self.fromAddress, self.toAddress, msg)

        # Close connection
        mailServer.quit()

# Helper functions for composing messages

## A function for directly composing the message in special circumstances
# @param subject Message subject
# @param body Message Body
# @returns Message to be passed to send


## Compose message to send
# @param zoneName The name of the zone updated
# @param successUpdate An array containing the ID of successfully updated zones (Array)
# @param failedUpdate An array containing the ID of zones that failed to update (Array)
# @param previousMessage The previous message composed (default to "") (String)
# @returns Message to be passed to Send module
def Compose(zoneName, successUpdate, failedUpdate, previousMessage = ""):
    message = previousMessage
    if len(successUpdate) != 0 or len(failedUpdate) != 0:
        message = message + zoneName + "\n"
        #Loop through each successful update message if at least one exists
        if len(successUpdate) != 0:
            #Add header message
            message = message + "   The following domains successfully updated:\n"
            #Loop through zones listing zone and IDs
            for domain in successUpdate:
                # Shouldn't occur but to catch a blank zone anyway
                if len(domain) != 0:
                    message = message + "       " + domain + "\n"

        #Loop through each failed update message if at least one exists
        if len(failedUpdate) != 0:
            #Add header message
            message = message + "   The following domains failed to update:\n"
            #Loop through zones listing zone and IDs
            for zone in failedUpdate:
                # Shouldn't occur but to catch a blank zone anyway
                if len(zone) != 0:
                    for id in zone:
                        message = message + "       " + id + "\n"

    #Return message
    return message

## A function to add to datetime and IP address to the footer of a message
# @param message The message to have the footer append to (String)
# @param currentIP The current IP address of the server (String)
# @param sendIP Include the IP address in the footer (Bool)
def Footer(message, currentIP, sendIP):

    #If sendIP address is true send the current IP address
    if sendIP:
        message = message + "The servers current IP address is: " + currentIP + ".\n"

    #Append date and time to message
    message = message + "This message was sent on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "."
    return message







