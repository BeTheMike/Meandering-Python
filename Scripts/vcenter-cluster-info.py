from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import atexit
import ssl
import requests
import getpass
from termcolor import cprint


# Collect User Info for vCenter
print('='*50)
vm_username = getpass.getuser() # Assumes vCenter login is the same as your machine account.
vm_password = getpass.getpass("vCenter (Domain) Password: ") # Assumes AD authentication
cSearch = input('Enter any part of a cluster name: ')  # Enter any part of the name of a cluster(s) you're looking for.
print('='*50, '\n')

# VM Functions


def GetCluster(info):
    #print("Getting ESXi Clusters...")
    host_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.ComputeResource],
                                                        True)
    obj = [cluster for cluster in host_view.view]
    host_view.Destroy()
    return obj


def GetVMHosts(info):
    #print("Getting all ESX hosts ...")
    host_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.HostSystem],
                                                        True)
    obj = [host for host in host_view.view]
    host_view.Destroy()
    return obj


def GetVMs(info):
    #print("Getting all VMs ...")
    vm_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.VirtualMachine],
                                                      True)
    obj = [vm for vm in vm_view.view]
    vm_view.Destroy()
    return obj

# Disabling urllib3 ssl warnings
requests.packages.urllib3.disable_warnings()

# Disabling SSL certificate verification
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_NONE

# Connect to vCenter
si = SmartConnect(
    host='Enter vCenter Info Here',
    user=vm_username,
    pwd=vm_password,
    port=443,
    sslContext=context)

# Disconnect vCenter
atexit.register(Disconnect, si)

# Here are the variables containing our vCenter Info
content = si.RetrieveContent()
clusters = GetCluster(content)
hosts = GetVMHosts(content)
vms = GetVMs(content)

cluster_name = []
cluster_name_sorted = sorted(cluster_name)
cluster_hosts = []
cluster_hosts_sorted = sorted(cluster_hosts)
vm_vlan_tags = []

for c in clusters:
    if cSearch in c.name:
        cluster_name.append(c.name)

if not cluster_name:
    print("No clusters match your search.\n")

for c in clusters:
    for cl in cluster_name:
        if cl == c.name:
            print("-"*80)
            cprint("Cluster Name: " + cl, 'red', attrs=['bold'])
            for h in c.host:
                f = si.content.customFieldsManager.field
                print(h.name)
                for k, v in [(x.name, v.value) for x in f for v in h.customValue if x.key == v.key]:
                    print("{}: {}".format(k, v))
                vm_vlan_tags.clear()
                for n in h.network:
                    try:
                        if 'DVUp' in n.name:
                            pass
                        else:
                            vm_vlan_tags.append(n.name.split('_')[1])
                    except:
                        pass
                try:
                    print('vCenter Tags:', ', '.join(sorted(vm_vlan_tags, key=int)))
                    print("-" * 80)
                except:
                    print(vm_vlan_tags)
                    print("-" * 80)
