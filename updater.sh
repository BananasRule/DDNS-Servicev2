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

cd /opt/DDNS-Servicev2

wget https://github.com/BananasRule/DDNS-Servicev2/releases/latest/download/latestversion.txt

# Get the version numbers from the latest release
read latest < latestversion.txt

# Use cut to split the string into three variables
latestMajor=$(echo $latest | cut -d '.' -f 1)
latestMinor=$(echo $latest | cut -d '.' -f 2)
latestPatch=$(echo $latest | cut -d '.' -f 3)

# Remove downloaded file
rm latestversion.txt

# Get the version numbers from the installed release
read current < version.txt

# Use cut to split the string into three variables
currentMajor=$(echo $current | cut -d '.' -f 1)
currentMinor=$(echo $current | cut -d '.' -f 2)
currentPatch=$(echo $current | cut -d '.' -f 3)

updaterequired=0

if [ $latestMajor -le $currentMajor ]
    then
    if [ $latestMinor -le $currentMajor ]
        then 
        if [ $latestPatch -le $currentPatch ]
            then echo "Program is up to date"
        else
            updaterequired=1
        fi
    else
        updaterequired=1
    fi
        
else 
    updaterequired=1
fi

if [ $updaterequired -eq 1 ]
    then
    echo "An update is available."
    echo "You have version: $current"
    echo "The latest version is: $latest"
    read -p "Would you like to update? (Y/N): " acceptance
    if [ ${acceptance^^} = "Y" ]
    then 
        echo "Updating now. Please do not stop process or power down your machine."
        # Remove existing data file
        rm -r data

        #Download and install new files overwriting old files
        wget https://github.com/BananasRule/DDNS-Servicev2/releases/latest/download/DDNS-Service-v2-Release.zip
        unzip -o DDNS-Service-v2-Release.zip 
        rm DDNS-Service-v2-Release.zip
    fi
fi

echo "Exiting updater"


