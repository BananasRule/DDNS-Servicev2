## © Jacob Gray 2022
## This Source Code Form is subject to the terms of the Mozilla Public
## License, v. 2.0. If a copy of the MPL was not distributed with this
## file, You can obtain one at http://mozilla.org/MPL/2.0/.

#External Dependencies
import logging, pickle, os, datetime
#Internal Dependencies
import APIAccessService, IPService, MessageService, ConfigLoadService, DataStorage
import MessageService

#Init Variables
criticalConfigFailure = False
mailConfigSuccess = False
mailMessage = ""

# Create logger
logging.basicConfig(
    filename="DDNSUpdateServiceLog.log",
    format='%(asctime)s %(levelname)s | %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

#Log run date and time
logger.info("Program started")

try:
    dnsSettings = ConfigLoadService.DNSConfigLoad()
except:
    logger.critical("Unable to load DNS Config.")
    dnsSettings = {}
    criticalConfigFailure = True

# Load DNS Settings in to variables

# Load IPv4 configuration
# Check that setting exists in dictionary
if "ipv4enabled" in dnsSettings:
    # Check for a valid value
    if dnsSettings["ipv4enabled"].upper() == "TRUE":
        ipv4 = True
    elif dnsSettings["ipv4enabled"].upper() == "FALSE":
        ipv4 = False
    else:
        # If no valid value is found default to false
        logger.warning("Unable to load IPv4 Configuration. Defaulting to True.")
        ipv4 = True
else:
    # If setting cannot be found default to IPv4
    logger.warning("Unable to find IPv4 Configuration. Defaulting to True.")
    ipv4 = True

# Load IPv6 configuration
# Check that setting exists in dictionary
if "ipv6enabled" in dnsSettings:
    # Check for a valid value
    if dnsSettings["ipv6enabled"].upper() == "TRUE":
        ipv6 = True
    elif dnsSettings["ipv6enabled"].upper() == "FALSE":
        ipv6 = False
    else:
        # If no valid value is found default to false
        logger.warning("Unable to load IPv6 Configuration. Defaulting to False.")
        ipv6 = False
else:
    # If setting cannot be found default to IPv4
    logger.warning("Unable to find IPv6 Configuration. Defaulting to False.")
    ipv6 = False

# Load user preference for sending IP Address in email
# Check that the setting exists in dictionary
# Defaults to false to prevent unintentional transmission of IP address over email
if "sendIP" in dnsSettings:
    if dnsSettings["sendIP"].upper() == "TRUE":
        sendIP = True
    elif dnsSettings["sendIP"].upper() == "FALSE":
        sendIP = False
    else:
        logger.warning("Unable to load Send IP Configuration. Defaulting to False.")
        sendIP = False
else:
    logger.warning("Unable to find Send IP Configuration. Defaulting to False.")
    sendIP = False

#Load zones as created in ConfigLoadService 
if "zones" in dnsSettings:
    #If no zones exits exit otherwise load
    if len(dnsSettings["zones"]) != 0:
        zones = dnsSettings["zones"]
    else:
        logger.critical("Unable to load any DNS Zones.")
        criticalConfigFailure = True
else:
    logger.critical("Error in config loader module.")
    criticalConfigFailure = True

#Load Mail Config File
mailSettings = None
try:
    mailSettings = ConfigLoadService.MailConfigLoad()
    mailConfigSuccess = True
except:
    logger.error("Unable to load mail config. Program will attempt to continue but will not send emails.")
    mailConfigSuccess = False

if mailConfigSuccess:
    # Attempt to load server address
    if "server" in mailSettings:
        mailHost = mailSettings["server"]
    else:
        logger.error("Unable to load mail server config. Program will attempt to continue but will not send emails.")
        mailConfigSuccess = False

    # Attempt to load port number
    if "port" in mailSettings:
        try:
            mailPort = int(mailSettings["port"])
        except:
            logger.error("Unable to load mail port config. Program will attempt to continue but will not send emails.")
            mailConfigSuccess = False
    else:
        logger.error("Unable to load mail port config. Program will attempt to continue but will not send emails.")
        mailConfigSuccess = False

    # Attempt to load TLS Setting
    if "TLS" in mailSettings:
        # Check for a valid value
        if mailSettings["TLS"].upper() == "TRUE":
            mailTLS = True
        elif mailSettings["TLS"].upper() == "FALSE":
            mailTLS = False
        else:
            # If no valid value is found default to false
            logger.warning("Unable to load TLS Configuration. Defaulting to False.")
            mailTLS = False
    else:
        # If setting cannot be found default to IPv4
        logger.warning("Unable to find TLS Configuration. Defaulting to False.")
        mailTLS = False

    # Attempt to load SSL Setting
    if "SSL" in mailSettings:
        # Check for a valid value
        if mailSettings["SSL"].upper() == "TRUE":
            mailSSL = True
        elif mailSettings["SSL"].upper() == "FALSE":
            mailSSL = False
        else:
            # If no valid value is found default to false
            logger.warning("Unable to load SSL Configuration. Defaulting to False.")
            mailSSL = False
    else:
        # If setting cannot be found default to IPv4
        logger.warning("Unable to find SSL Configuration. Defaulting to False.")
        mailSSL = False

    # Attempt to load mail from address
    if "fromAddress" in mailSettings:
        mailFromAddress = mailSettings["fromAddress"]
        # Rudimentary valid email check. Won't stop invalid email.
        if ("@" in mailFromAddress) == False:
            logger.warning("From email address does not contain @ symbol. Please check address.")
    else:
        logger.error(
            'Unable to load mail from address config. Program will attempt to continue but will not send emails.')
        mailConfigSuccess = False

    # Attempt to load mail to address
    if "toAddress" in mailSettings:
        mailToAddress = mailSettings["toAddress"]
        # Rudimentary valid email check. Won't stop invalid email.
        if ("@" in mailToAddress) == False:
            logger.warning("To email address does not contain @ symbol. Please check address.")
    else:
        logger.error(
            'Unable to load mail to address config. Program will attempt to continue but will not send emails.')
        mailConfigSuccess = False

    # Attempt to load mail key
    if "key" in mailSettings:
        mailKey = mailSettings["key"]
    else:
        logger.error(
            'Unable to load mail key config. Program will attempt to continue but will not send emails.')
        mailConfigSuccess = False

    # Attempt to load mail secret
    if "secret" in mailSettings:
        mailSecret = mailSettings["secret"]
    else:
        logger.error(
            'Unable to load mail secret config. Program will attempt to continue but will not send emails.')
        mailConfigSuccess = False

## DDNS Update Section ## 

# Create mail server class if setup succeeded 
if mailConfigSuccess:
    try:
        mailServer = MessageService.Messenger(mailHost, mailPort, mailKey, mailSecret, mailTLS, mailSSL, mailFromAddress, mailToAddress)
    except:
        # In the event of a setup failure attempt to proceed without email
        mailConfigSuccess = False
        logger.error("Failed to connect to mail server. Program will continue.")

# Check for a critical failure in config
if criticalConfigFailure:
    logger.critical("A critical failure was detected.")
    if mailConfigSuccess:
        
        dataFilename = "data/EDDNS.data"
        # Attempt to load error datafile
        # This is used to stop a spam of error messages as only one per hour should be sent
        if not os.path.isdir("data"):
            os.mkdir("data")
        if os.path.exists(dataFilename):
            datafile = open(dataFilename, "rb")
            try:
                store = pickle.load(datafile)
            except:
                # Check exceptions if data file is corrupt
                store = DataStorage.Store()
            datafile.close()
        else:
        # Otherwise create a new store class
            store = DataStorage.Store()
        
        # Check if an email with the same status code was not sent in the same hour
        if store.runHour != datetime.datetime.now().hour and store.status != 99:
            mailMessage = "A critical error occurred. Please see log files for more info. The program did not run.\nThis message was sent at: " \
                + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "."
            mailServer.Send("DDNS Service had critical failure", mailMessage)
            logger.critical("An email advising of the critical error was sent.")

            # Save updated details to store if email was sent
            # This should allow for retries if email did not send
            store.runHour = datetime.datetime.now().hour
            store.status = 99
            savefile = open(dataFilename, "wb")
            pickle.dump(store, savefile)
            savefile.close

    logger.critical("The program will now exit.")


else:

    ## Define the common updater for both IPv4 and v6
    # Not intended to be a standalone function as it uses previously defined variables
    # This just helps simplify code maintenance for ipv4/6 variants as the only differ slightly
    # Treat this function as if it was just in the main section 
    def Updater(isipv4):
        
        #Initalise variables
        if isipv4:
            dataFilename = "data/DDNS.data"
        else:
            dataFilename = "data/DDNS6.data"
        successfulUpdates = []
        failedUpdates = []
        subject = ""
        mailMessage = ""
        failedZones = []
        store = None

        # Check that data directory exists, if not create it
        if not os.path.isdir("data"):
            os.mkdir("data")
        
        # If a data store already exits load it
        if os.path.exists(dataFilename):
            datafile = open(dataFilename, "rb")
            try:
                store = pickle.load(datafile)
            except:
                # Check exceptions if data file is corrupt
                store = DataStorage.Store()
            datafile.close()
        else:
            # Otherwise create a new store class
            store = DataStorage.Store()

        # Attempt to get current IP address
        try:
            currentIP = IPService.Get(True)
        except:
            # Send email about IP address resolution failure if mail is configured and the previous run didn't have this issue
            # or the previous run was last hour
            if (store.status != 2 or datetime.datetime.now().hour != store.runHour()) and mailConfigSuccess == True:
                mailServer.Send("IP Address Error", "An error occurred determining IP Address.\nThis email was sent at " \
                    + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            logger.critical("Error in determining IPv4 Address. Exiting Program")
            exit()

        # Check if current IP address matches stored IP and run occurred in the last hour
        # This is done to limit Cloudflare API calls and allows a more frequent run time
        # as the IP address APIs do not have limits (or are so high they don't matter)
        if currentIP == store.ipAddress and datetime.datetime.now().hour == store.runHour and store.status == 0:
            logger.info("Current IP address matches previous run and the previous run occurred within the same hour. Exiting Program")
        else:
            # If IP address needs updating loop through zones as defined in the config file
            for zone in zones:
                try:
                    # Call APIAccessService and attempt to update zone
                    APIService = APIAccessService.AccessService(zone.apiKey, zone.id)
                    status = APIService.UpdateRecords(currentIP, zone.list, zone.listType, isipv4)
                    #Create message for email by adding to previous message
                    mailMessage = MessageService.Compose(zone.name, status[0], status[1], mailMessage)
                    #Add successes and failures to overall list
                    successfulUpdates = successfulUpdates + status[0]
                    failedUpdates = failedUpdates + status[1]
                except:
                    mailMessage = mailMessage + zone.name + ' - Failed to access zone\n'
                    failedUpdates = failedUpdates + ["zone:"+zone.name]
                    logger.error("Failed accessing API and updating records (Zone Name: " + zone.name + ")")

            if len(successfulUpdates) != 0 or len(failedUpdates) != 0:
                # Define email subject and leave log depending on if any items failed
                if len(failedUpdates) == 0:
                    subject = "DNS Records Successfully Updated"
                    logger.info("Domains successfully updated")
                else:
                    subject = "DNS Records Failed To Update"
                    logger.warning("Domains failed to update")
            else:
                # If no items changed in the run log that outcome
                #The subject shouldn't be called but this is a fallback -
                subject = "DNS Records Not Updated"
                logger.info("Domains were checked but none needed updating")

            
            #Send email to user if configured correctly
            if mailConfigSuccess:
                #Check that email is not empty
                if len(successfulUpdates) != 0 or len(failedUpdates) != 0:
                    #Check that an identical email was not previously sent or was sent in the previous hour
                    if not(successfulUpdates == store.succeeded and failedUpdates == store.failed and datetime.datetime.now().hour == store.runHour):
                        try:
                            #Create email footer 
                            mailMessage = MessageService.Footer(mailMessage, currentIP, sendIP)
                            #Send email
                            mailServer.Send(subject, mailMessage)
                            logger.info("Email Sent")
                        except:
                            logger.error("Email failed to send")

            
            # Store information for next run
            store.ipAddress = currentIP
            store.runHour = datetime.datetime.now().hour
            store.succeeded = successfulUpdates
            store.failed = failedUpdates
            if len(failedUpdates) == 0:
                store.status = 0
            else:
                store.status = 1
            
            #Save store class
            
            savefile = open(dataFilename, "wb")
            pickle.dump(store, savefile)
            savefile.close()

    # Call above function for ipv4/6 if specified in config file
    if ipv4:
        Updater(True)

    if ipv6:
        Updater(False)
