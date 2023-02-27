# DDNS-SERVICEv2
## DDNS Service for use with Cloudflare®

### THIS APPLICATION IS NOT ENDORSED, SPONSORED OR ASSOCIATED WITH CLOUDFLARE
### THIS APPLICATION USES THE CLOUDFLARE API V4

### Use of this application is subject to the terms of the license

<br>

This is a python program designed to update DNS records stored with Cloudflare for environments with am dynamic IP address. This program is designed to support multiple DNS zone. If a signifiant event (record update, record update failure, config failure) occurs it will notify you via Email using SMTP. 

It is designed to run once a minute and will check the IP address against the previous run's IP address. If it differs, it has been more then one hour since the last run or the last run was a failure it will check the IP address of the DNS records and update them if necessary.

# One click install
Run the following command to install the software
```
wget https://raw.githubusercontent.com/BananasRule/DDNS-Servicev2/main/installer.sh && sudo bash installer.sh 
 ```

# Licence
This program is licensed under MPL2.0. Please also include the attribution '© Jacob Gray 2022'. Please see LICENSE.txt for information.

# Acknowledgements
This software uses the requests library licensed under the Apache License 2.0

    Requests
    Copyright 2019 Kenneth Reitz

This software uses libraries from the standard python library under the PSF LICENSE AGREEMENT

    Copyright © 2001-2022 Python Software Foundation; All Rights Reserved

Cloudflare, the Cloudflare logo, and Cloudflare Workers are trademarks and/or registered trademarks of Cloudflare, Inc. in the United States and other jurisdictions.


 
