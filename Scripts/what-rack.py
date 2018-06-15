from jnpr.junos import Device
from jnpr.junos.op.arp import ArpTable
from jnpr.junos.op.lldp import LLDPNeighborTable
import re
import sys
import socket
import getpass

"""This script will take an IP, do a DNS lookup if necessary
and with that IP, ID via the ARP table what interface the arp
resides on to quickly ID what ToR it's connected to in the DC."""

whatIP = sys.argv[1]

#Sets a test to make sure it looks like an IP.  Yes, non IP values could match
#but this works well for what I need it for.
pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
testIP = pat.match(whatIP)

if testIP:
    findIP = whatIP #If it matches IP format, just carry on and set the variable.
else:
    findIP = socket.gethostbyname(whatIP) #If it's anything else, try and do a DNS lookup on it.
    print ('Looking for IP: '+ findIP)

# Log into the switch
hostname = input("Switch IP: ")
username = input("Username: ")
password = getpass.getpass("Password: ")
dev = Device(host=hostname, user=username, passwd=password)
dev.open()

# Get ARP Info
arp = ArpTable(dev)
arp.get()
arp_list = arp.values()

# Get LLDP Info
lldp = LLDPNeighborTable(dev)
lldp.get()
lldp_list = lldp.values()

key = findIP

for mac, ip, interface in arp_list:
    if key in ip:
        for clean in interface:
            int_clean = re.search(r'ae[0-9]{1,2}', str(clean))
            if int_clean:
                ae_int = int_clean.group(0)
                for local_int, local_parent, remote_type, remote_chassis, remote_desc, remote_id, remote_sysname in lldp_list:
                    if ae_int in local_parent:
                        print("IP = {}, Mac = {}, Rack = {}".format(str(findIP), mac[1], remote_sysname[1]))
                        print("")

dev.close()
