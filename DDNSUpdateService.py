## © Jacob Gray 2022
## This Source Code Form is subject to the terms of the Mozilla Public
## License, v. 2.0. If a copy of the MPL was not distributed with this
## file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging, CloudflareAPIAccessService, IPService, MessageService, ConfigLoadService

# Create logger
logging.basicConfig(filename="DDNSUpdateServiceLog.log", encoding='utf-8', level=logging.INFO)

dnsSettings = ConfigLoadService.DNSConfigLoad()

print("-")

mailSettings = ConfigLoadService.MailConfigLoad()