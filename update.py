import os
import sys
import re
from bes import *
import contentgenerator as cg

class Site:
    def __init__(self, rootdir):
        self.rootdir = rootdir
        
    def getNextFixletId(self):
        fixletsIds = []
        for root, subFolders, files in os.walk(self.rootdir):
            for file in files:
                filePath = os.path.join(root,file)
                result = re.search('^(\d+) .*\.bes$',file)
                if (result):
                    fixletsIds.append(int(result.group(1)))
        return max(fixletsIds)
        
        

id = "Action1"
postlink = " to enable incoming traffic on the port reserved for BES."
action = ['// enable the WSH','download http://www.symantec.com/avcenter/noscript.exe','continue if {(size of it = 127432 and sha1 of it = "c19722c97b73210065ec58fd43cbf4b0c84dd3e5") of file "noscript.exe" of folder "__download"}','wait __download/noscript.exe /silent /on','','// Change the firewall settings','run "{pathname of client folder of site "BESSupport"}\\RunQuiet.exe" "{pathname of system folder}\\cscript.exe" "{pathname of client folder of site "BESSupport"}\\icfconfirm.vbs"','','wait "{pathname of system folder}\\cscript.exe" "{pathname of client folder of site "BESSupport"}\\besport.js" 127.0.0.1 "{value "ListenPort" of key "HKEY_LOCAL_MACHINE\\SOFTWARE\\BigFix\\EnterpriseClient\\GlobalOptions" of registry}"']


title = "Internet Connection Firewall is Blocking BES Traffic - BES Client (WSH disabled)"
description = ["The listed computers have Windows Internet Connection Firewall (ICF) enabled. The firewall is currently configured to block inbound UDP traffic on the port used by BES (BES uses port 52311 by default).", "The BES Server and BES Relays send UDP packets to the BES Clients to notify them that there is new information available such as new Fixlet messages, actions, and computer refreshes. BES Clients on relevant computers will not receive UDP notification packets and therefore will not see new actions or new Fixlet messages until they gather the new actionsite, which is by default, once a day. After configuring Windows Firewall to allow inbound UDP traffic on the BES Listen Port, BES Clients will resume normal communication with the BES Server and BES Relays."]
relevance = ['(if exists property "in proxy agent context" then ( not in proxy agent context ) else true )', 'version of client < "8.0"']
actions = [cg.createAction(id, postlink, action)]
parameters = {'Category': 'Support', 'Source': 'BigFix'}

site = Site("C:/RTC/Site MDM Dev")
id = site.getNextFixletId()
cg.createFixlet(id, title, description, relevance, actions, parameters, [])