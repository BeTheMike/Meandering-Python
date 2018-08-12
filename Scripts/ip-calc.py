import ipcalc
import sys

# Pull address from input
# addrString = raw_input("Address (x.x.x.x/x): ")
addrString = sys.argv[1]

#Pull netmask
subnet = ipcalc.Network(addrString)
# Generate empty list
AddrList = []
# Append items to the list
for x in ipcalc.Network(addrString):
   AddrList.append(str(x))
# Print it out all pretty-like
print("Network: " , str(subnet.network()))
print("Address Range: " , AddrList[0], " - " , AddrList[-1])
print("Usable Addresses: ", len(AddrList))
print("Netmask: " , str(subnet.netmask()))