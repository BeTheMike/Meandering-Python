import re
import sys
import socket
import getpass
from lxml import etree
import jxmlease
from jnpr.junos import Device

"""This script will take an IP, log into a given switch, and give you the active VTEP it's 
source from.  It ouputs:

[A Record of the IP] - [IP address you searched for]
[MAC address of the server or device] - [VTEP It's currently source from]

It assumes that your spine/leaf are your VTEPs and does rely heavily on DNS for usable info """

def rev_dns(ip_address): # Does a reverse lookup on an IP
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except:
        return ip_address

def ip_lookup(user_input): # Forward lookup on an IP.  Tries to resolve the DNS name if available.
    pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    lookup_ip = pat.match(user_input)
    if lookup_ip:
        #print('Looking up: ', rev_dns((lookup_ip)))
        return user_input
    else:
        try:
            lookup_ip = socket.gethostbyname(user_input)
            #print("Looking for: ", user_input, "IP - ", lookup_ip)
            return lookup_ip
        except socket.gaierror:
            print("")
            print("No DNS Entry exists for that host - exiting script")
            print("")
            sys.exit()

def do_search(): # Performing the actual EVPN lookup.
    for device in evpn_parsed['evpn-database-information']['evpn-database-instance']['mac-entry']:
        if device.get('ip-address') == whatIP:
            print("{:<15} - {:<40}".format(rev_dns(device.get('ip-address')), device.get('ip-address')))
            print("Mac: {:<15} - ToR: {:<40}\n".format(device.get('mac-address'), rev_dns(device.get('active-source'))))

# Login info for the switch
switch_ip = input("Switch IP: ")
switch_user = input("Username: ")
switch_pass = getpass.getpass("Password: ")

for x in sys.argv[1:]:
    whatIP = ip_lookup(x)
    try:
        with Device(host=switch_ip, user=switch_user, password=switch_pass, timeout=300) as dev:
            evpn = dev.rpc.get_evpn_database_information()
            evpn_parsed = jxmlease.parse(etree.tostring(evpn, encoding='unicode'))
            do_search()
    except Exception as e:
        print(e)

