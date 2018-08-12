import re
import sys
import socket
import getpass
from lxml import etree
import jxmlease
from jnpr.junos import Device


def ip_lookup(user_input):
    pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    lookup_ip = pat.match(user_input)
    if lookup_ip:
        print('Looking up: ', rev_dns((lookup_ip)))
        return lookup_ip
    else:
        try:
            lookup_ip = socket.gethostbyname(user_input)
            print("Looking for: ", user_input, "IP - ", lookup_ip)
            return lookup_ip
        except socket.gaierror:
            print("")
            print("No DNS Entry exists for that host - exiting script")
            print("")
            sys.exit(1)

def rev_dns(ip_address):
    try:
        #ip_address = "'{}'".format(ip_address)
        return socket.gethostbyaddr(ip_address)[0]
    except:
        #ip_address = "'{}'".format(ip_address)
        return ip_address

def local_ip_clean(local_ip):
    try:
        str = local_ip.split("+")
        return str[0]
    except:
        return local_ip

def peer_status(status):
    if status == 'Connect':
        return 'Con'
    elif status == 'Active':
        return 'Act'
    elif status == 'Established':
        return 'Est'
    else:
        return (status)

def my_Sort(s):
    return s[-3:]

def peer_full():
    try:
        # Log into the switch
        hostname = ip_lookup(input('IP or Hostname of device: '))
        username = input('Username: ')
        password = getpass.getpass('Password: ')

        dev = Device(host=hostname, user=username, passwd=password, gather_facts=False)
        dev.open()

        conf = dev.rpc.get_config()
        conf_parsed = jxmlease.parse(etree.tostring(conf, encoding='unicode'))

        routing_instances = []
        try:
            for r_instance in conf_parsed['configuration']['routing-instances']['instance']:
                routing_instances.append((r_instance['name'].get_cdata()))
        except:
            routing_instances.append('Empty')

        sorted_instances = sorted(routing_instances, key=my_Sort)

        for instance in sorted_instances:
            if 'Empty' not in sorted_instances:
                try:
                    rpc = dev.rpc.get_bgp_summary_information(instance=instance)
                    result = jxmlease.parse(etree.tostring(rpc, pretty_print=True, encoding='unicode'))
                    print('Routing Instance: ', instance)
                    for neighbor in result['bgp-information']['bgp-peer']:
                        print(neighbor['peer-as'] + ":" + rev_dns(neighbor['peer-address']) + '({})'.format(
                            neighbor['peer-address']),
                              "[" + peer_status(neighbor['peer-state']), neighbor['elapsed-time'] + "]")
                    else:
                        pass
                except:
                    pass
            else:
                rpc = dev.rpc.get_bgp_summary_information()
                result = jxmlease.parse(etree.tostring(rpc, pretty_print=True, encoding='unicode'))
                for neighbor in result['bgp-information']['bgp-peer']:
                    print(neighbor['peer-as'] + ":" + rev_dns(neighbor['peer-address']),
                          "[" + peer_status(neighbor['peer-state']),
                          neighbor['elapsed-time'] + "]")

        dev.close()
    except:
        sys.exit('Bad password.  Exiting')

def peer24h():
    try:
        # Log into the switch
        hostname = input('IP or Hostname of device: ')
        username = input('Username: ')
        password = getpass.getpass('Password: ')

        dev = Device(host=hostname, user=username, passwd=password, gather_facts=False)
        dev.open()

        print('\n'*3)
        print('This may take a second...')
        print('\n'*3)

        conf = dev.rpc.get_config()
        conf_parsed = jxmlease.parse(etree.tostring(conf, encoding='unicode'))

        routing_instances = []
        try:
            for r_instance in conf_parsed['configuration']['routing-instances']['instance']:
                routing_instances.append((r_instance['name'].get_cdata()))
        except:
            routing_instances.append('Empty')

        sorted_instances = sorted(routing_instances, key=my_Sort)
        clean_instances = []

        for instance in sorted_instances:
            if 'Empty' not in sorted_instances:
                try:
                    rpc = dev.rpc.get_bgp_summary_information(instance=instance)
                    result = jxmlease.parse(etree.tostring(rpc, pretty_print=True, encoding='unicode'))
                    for neighbor in result['bgp-information']['bgp-peer']:
                        if 'd' not in neighbor['elapsed-time']:
                            clean_instances.append(instance)
                except:
                    pass
            else:
                rpc = dev.rpc.get_bgp_summary_information()
                result = jxmlease.parse(etree.tostring(rpc, pretty_print=True, encoding='unicode'))
                for neighbor in result['bgp-information']['bgp-peer']:
                    if 'd' not in neighbor['elapsed-time']:
                        print(neighbor['peer-as'] + ":" + rev_dns(neighbor['peer-address']),
                              "[" + peer_status(neighbor['peer-state']),
                              neighbor['elapsed-time'] + "]")

        final_instances = (list(set(clean_instances)))
        sorted_final_instances = sorted(final_instances, key=my_Sort)

        for instance in sorted_final_instances:
            if not sorted_final_instances:
                pass
            else:
                print('Routing Instance: ', instance)
                rpc = dev.rpc.get_bgp_summary_information(instance=instance)
                result = jxmlease.parse(etree.tostring(rpc, pretty_print=True, encoding='unicode'))
                for neighbor in result['bgp-information']['bgp-peer']:
                    if 'd' not in neighbor['elapsed-time']:
                        print(neighbor['peer-as'] + ":" + rev_dns(neighbor['peer-address']) + '({})'.format(
                            neighbor['peer-address']), "[" + peer_status(neighbor['peer-state']),
                              neighbor['elapsed-time'] + "]")
                else:
                    pass

        dev.close()
    except:
        sys.exit('Bad password.  Exiting')

def peer_established():
    try:
        # Log into the switch
        hostname = input('IP or Hostname of device: ')
        username = input('Username: ')
        password = getpass.getpass('Password: ')

        dev = Device(host=hostname, user=username, passwd=password, gather_facts=False)
        dev.open()

        print('\n'*3)
        print('This may take a sec...')
        print('\n'*3)

        conf = dev.rpc.get_config()
        conf_parsed = jxmlease.parse(etree.tostring(conf, encoding='unicode'))

        routing_instances = []
        try:
            for r_instance in conf_parsed['configuration']['routing-instances']['instance']:
                routing_instances.append((r_instance['name'].get_cdata()))
        except:
            routing_instances.append('Empty')

        sorted_instances = sorted(routing_instances, key=my_Sort)
        clean_instances = []

        for instance in sorted_instances:
            if 'Empty' not in sorted_instances:
                try:
                    rpc = dev.rpc.get_bgp_summary_information(instance=instance)
                    result = jxmlease.parse(etree.tostring(rpc, pretty_print=True, encoding='unicode'))
                    for neighbor in result['bgp-information']['bgp-peer']:
                        if 'Established' not in neighbor['peer-state']:
                            clean_instances.append(instance)
                        else:
                            pass
                except:
                    pass
            else:
                rpc = dev.rpc.get_bgp_summary_information()
                result = jxmlease.parse(etree.tostring(rpc, pretty_print=True, encoding='unicode'))
                for neighbor in result['bgp-information']['bgp-peer']:
                    if 'Established' not in neighbor['peer-state']:
                        print(neighbor['peer-as'] + ":" + rev_dns(neighbor['peer-address']),
                              "[" + peer_status(neighbor['peer-state']),
                              neighbor['elapsed-time'] + "]")

        final_instances = (list(set(clean_instances)))
        sorted_final_instances = sorted(final_instances, key=my_Sort)

        for instance in sorted_final_instances:
            if not sorted_final_instances:
                pass
            else:
                print('Routing Instance: ', instance)
                rpc = dev.rpc.get_bgp_summary_information(instance=instance)
                result = jxmlease.parse(etree.tostring(rpc, pretty_print=True, encoding='unicode'))
                for neighbor in result['bgp-information']['bgp-peer']:
                    if 'Established' not in neighbor['peer-state']:
                        print(neighbor['peer-as'] + ":" + rev_dns(neighbor['peer-address']) + '({})'.format(
                            neighbor['peer-address']), "[" + peer_status(neighbor['peer-state']),
                              neighbor['elapsed-time'] + "]")
                else:
                    pass

        dev.close()
    except:
        sys.exit('Bad password.  Exiting')
def main():

    choice = '0'
    while choice =='0':
        print('1. Full BGP Peers\n2. Partial - Non-Established Only\n3. Partial - Less Than 24 Hours\n4. Exit')

        choice = input("Please select an option: ")

        if choice == '4':
            sys.exit('Exiting Script')
        elif choice == '3':
            peer24h()
        elif choice == '2':
            peer_established()
        elif choice == '1':
            peer_full()
        else:
            print("Please pick a valid option")

if __name__ == '__main__':
    main()
