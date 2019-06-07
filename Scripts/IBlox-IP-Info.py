#!/usr/bin/env python
import ipcalc
import json
import re
import sys
import socket
import getpass
import requests
from termcolor import colored, cprint
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable the HTTPS warning ... for now
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main(argv):

    while True:
        try:
            # User Info
            user = getpass.getuser()  # Assumes your compuer login is the same as your InfoBlox login
            password = getpass.getpass("Enter Infoblox Password: ")
            IBlox = 'Your InfoBlox Info Here'  ## Put your Infoblox DNS name or IP here.

            for x in argv[1:]:
                whatIP = x
                #Sets a test to make sure it looks like an IP.  Yes, non IP values could match
                #but this works well for what I need it for.
                pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
                testIP = pat.match(whatIP)

                if testIP:
                    ip_address = whatIP #If it matches IP format, just carry on and set the variable.
                else:
                    try:
                        ip_address = socket.gethostbyname(whatIP) #If it's anything else, try and do a DNS lookup on it.
                        print("Looking for: ", x, "IP - ", ip_address)
                    except socket.gaierror:
                        print("")
                        print("No DNS Entry exists for that host - exiting script")
                        print("")
                        sys.exit()
                print('')
                api_url_ip = requests.get('https://' + IBlox + '/wapi/v1.4.2/ipv4address?ip_address=' + ip_address, auth=(user,password), verify=False)
                api_url_network = requests.get('https://' + IBlox + '/wapi/v1.4.2/network?contains_address=' + ip_address, auth=(user,password), verify=False)
                ip_data = json.loads(api_url_ip.text)
                network_data = json.loads(api_url_network.text)

                #Uncomment below if you want to see the output of what JSON is pulling.
                #print (json.dumps(ip_data))

                def getNames(api_get_data):
                    for string in api_get_data:
                        return string['names']

                def getNetwork(api_get_data):
                    if 'Error' in api_get_data:
                        print("")
                        print("No network for this IP exists.  Exiting")
                        print("")
                        sys.exit()
                    else:
                        for network in api_get_data:
                            return network.get('network')

                def getNetName(api_get_data):
                    for net_name in (api_get_data):
                        return net_name.get('comment')

                def getREF(api_input_ref):
                    decode = json.loads(api_input_ref.text)
                    for ref in decode:
                        new_net_ref = ref['_ref']
                        return new_net_ref

                def getType(api_get_data):
                    for type in api_get_data:
                        return type.get('types')

                def getEXT(api_input_ref):
                    if "N/A" in api_input_ref:
                        pass
                    else:
                        decode = json.loads(api_input_ref.text)
                        if 'extattrs' in decode:
                            for attribute, value in decode['extattrs'].items():
                                if attribute:
                                    for second, val in value.items():
                                        if '_ref' in str(val):
                                            pass
                                        else:
                                            print(attribute, "=", val)
                                else:
                                    pass
                        else:
                            pass

                network_address = getNetwork(ip_data)
                net_ref = getREF(api_url_network)

                # Now let's get the attributes for the IP and Network
                net_extattr_get = requests.get('https://' + IBlox + '/wapi/v2.7/' + net_ref + '?_return_fields%2B=extattrs&*', verify=False, auth=(user,password))

                # Below is the info that build the IP list from the above NetMRI gets.
                subnet = ipcalc.Network(getNetwork(ip_data))
                # Generate empty list
                AddrList = []
                # Use the calculator to build a list of all the IP addresses
                for x in ipcalc.Network(getNetwork(ip_data)):
                    AddrList.append(str(x))

                print('')
                print('#' * 70)
                print('')
                print('IP ' + ip_address + ' is part of ' + getNetwork(ip_data))
                print('Network: ', str(subnet.network()) + " | " + "Range: ", AddrList[0], " - ", AddrList[-2] + " | " + "Usable: ", len(AddrList))
                print('Network Mask: ', str(subnet.netmask()), "|", " Default GW:", AddrList[-1])
                print('Network Comment: ' + '"{}"'.format(getNetName(network_data)))
                print('')
                cprint('Network Attributes:', 'red', attrs=['bold'])
                getEXT(net_extattr_get)
                print('-' * 70)
                if 'A' in getType(ip_data):
                    cprint('The DNS names associated with  ' + ip_address + ' are:', 'red', attrs=['bold'])
                    print('\n'.join(str(p) for p in getNames(ip_data)))
                else:
                    cprint('The DNS names associated with  ' + ip_address + ' are:', 'red', attrs=['bold'])
                    print('No DNS records associated with this IP')
                print('')
                print('#' * 70)
                sys.exit()

        except ValueError:
            print("Incorrect Infoblox Password - Try Again")

if __name__ == "__main__":
    main(sys.argv)