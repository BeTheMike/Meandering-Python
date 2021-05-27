import os
import datetime
import socket
import getpass
import sys
import re
from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos import Device
from jnpr.junos.utils.scp import SCP
from jnpr.junos.utils.fs import FS
from termcolor import cprint
from lxml import etree


def rev_dns(ip_address):  # Perform a reverse lookup on the IP if available.
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except:
        return ip_address


def dns_lookup(lookup):  # Return an IP based on a lookup or just return the IP.
    pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    ip_check = pat.match(lookup)
    if ip_check:
        return lookup
    else:
        try:
            ip_check = socket.gethostbyname(lookup)
            return ip_check
        except socket.gaierror as err:
            missedEquipment[lookup] = "No DNS Entry Exists - Skipping"


def get_rsi(equipment):
    try:
        print("Gathering RSI...(This takes a bit - give it time. Timeout is 10 minutes.)")
        ss = StartShell(equipment)
        ss.open()
        ss.run('cli request support information \\| save /var/tmp/' + current_date + '_py_rsi.txt', this="%",
               timeout=600)
        print("RSI Done, copying it and deleting it...\n")
        ss.close()
        with SCP(equipment, progress=True) as scp:
            scp.get('/var/tmp/' + current_date + "_py_rsi.txt", full_file + "_" + current_date + "_rsi.txt")
        fileSystem = FS(equipment)
        fileSystem.rm('/var/tmp/*_py_rsi.txt')
    except Exception as err:
        missedEquipment[equipment] = "Error getting RSI - " + str(err)


def get_config_set(equipment):
    try:
        print("Gathering Config in Set format\n")
        config_set = equipment.rpc.get_config(options={'format': 'set', 'database': 'committed'})
        with open(f"{full_file}-Set-[{current_date}].txt", "w") as w:
            w.write(etree.tostring(config_set, encoding='unicode'))
    except Exception as err:
        missedEquipment[equipment] = "Error getting Config_Set - " + str(err)


def get_logs(equipment):
    try:
        print("Compressing /var/log...")
        fileSystem = FS(equipment)
        fileSystem.tgz("/var/log/*", "/var/tmp/" + current_date + "_py_varlog.tgz")
        print("Copying log files down and removing the .tgz that was created...")
        with SCP(equipment, progress=True) as scp:
            scp.get(f"/var/tmp/" + current_date + "_py_varlog.tgz", full_file + "_" + current_date + "_varlog.tgz")
        print("\nRemoving that var/log file\n")
        fileSystem.rm("/var/tmp/*_py_varlog.tgz")
    except Exception as err:
        missedEquipment[equipment] = "Error getting logs - " + str(err)


# Collect Device Password
dev_user = input("Device Username: ")
dev_password = getpass.getpass("Enter device passwords: ")

# Get date/time
now = datetime.datetime.now()
current_date = now.strftime("%m-%d-%Y")

# Set File path
file_path = os.path.expanduser('~/Documents/_Device-Backups')
if not os.path.exists(file_path):
    os.makedirs(file_path, exist_ok=True)

missedEquipment = {}

for equip in sys.argv[1:]:
    try:
        cprint(f"Connecting to {rev_dns(equip)} - {dns_lookup(equip)}", 'red', attrs=['bold', 'underline'])
        with Device(host=dns_lookup(equip), user=dev_user, password=dev_password) as dev:
            dev.timeout = 300
            full_file = os.path.join(file_path, rev_dns(equip))
            get_config_set(dev)
            get_logs(dev)
            get_rsi(dev)
    except Exception as err:
        missedEquipment[equip] = str(err)
        pass

if len(missedEquipment) != 0:
    cprint('\nEquipment that was skipped:', 'red', attrs=['bold', 'underline'])
    for k, v in missedEquipment.items():
        print(k, v)
else:
    cprint('No equipment skipped.  Script complete.', 'red', attrs=['bold', 'underline'])
print("")
