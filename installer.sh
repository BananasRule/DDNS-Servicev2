#!/bin/bash

## © Jacob Gray 2022
## This Source Code Form is subject to the terms of the Mozilla Public
## License, v. 2.0. If a copy of the MPL was not distributed with this
## file, You can obtain one at http://mozilla.org/MPL/2.0/.

#Check that script is running as root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi


#License agreement
#Make user aware under which license they are installing the software and get their agreement
echo "Preparing to install DDNS-Service"
echo "Please agree to the license terms to continue: "
echo "This software is licenced under MPL2.0, a copy of which can be found here: https://github.com/BananasRule/DDNS-Servicev2/blob/main/LICENSE.txt"
echo "This license includes a disclaimer of warranty and limitation of liability."
echo "By agreeing you explicitly agree to the disclaimer of warranty and limitation of liability in addition agreeing to the full license."
echo "By agreeing you declare you have read, understood and have the capability to enter into and agree this license."
#Force user to read above paragraph
sleep 5
#Check acceptance with agreement
read -p "Do you agree to the license terms? (Y/N): " acceptance
acceptance=${acceptance^^}
if [ ${acceptance} = "Y" ]
then
#Install dependencies 
echo "Thank you for agreeing to the license terms. Installation will now begin."
apt update
apt upgrade -y
apt install unzip -y
apt install python3 -y
apt install python3-pip -y
pip install requests 

#Create folder
cd /opt
mkdir DDNS-Servicev2
cd DDNS-Servicev2
#Download software from latest release and unzip
wget https://github.com/BananasRule/DDNS-Servicev2/releases/latest/download/DDNS-Service-v2-Release.zip
unzip DDNS-Service-v2-Release.zip 
rm DDNS-Service-v2-Release.zip

#Create directory config and copy example files
mkdir config
cp example_dnsconfig.conf config/dnsconfig.conf
cp example_mailconfig.conf config/mailconfig.conf
#Open example files for user to enter data to
cd config
nano dnsconfig.conf
nano mailconfig.conf

#Protect folder from unauthorised access
cd /opt
chmod 700 -R DDNS-Servicev2

#Add cronjob to run every minute
crontab -l > tempcron
echo "* * * * * cd /opt/DDNS-Servicev2 && python3 /opt/DDNS-Servicev2/DDNSUpdateService.py" >> tempcron
crontab tempcron
rm tempcron
service cron restart

echo "Installation complete"

fi
