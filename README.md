# Meandering-Python
Trying to catch the dev/automation/scripting train while laying on the tracks.


#### Some short descriptions on scripts:

**dhcp-usage.py**: Quick little script that will scour DHCP ranges and kick back any range that is reported above 60% utilization.

**IBlox-IP-Info.py**: Does an API lookup for a hostname or IP against your Infoblox database.
It will give you all the subnet info for the IP as well as ny Network Attributes assigned to it as well as if there are one
or multiple "A" records.

**single-string-cleanup.py**
This will iterate through a directory structure (just text files) looking for whatever string you put in and replace it 
with whatever you want it replaced with.  It will prompt you for the directory.  It will then give you a list of directories
that it found that string in and give you a chance to cancel out of the replace in case something doesn't look right.

**what-rack.py** 
Pretty specific script.  This will connect to a Juniper device, look for a specific IP and pull the current VTEP that is being routed from. 

**ip-calc.py**:  Basic IP calculator to give you the IP info based on a CIDR range and mask (i.e. 10.3.3.3/26)

**bgp-peers.py**:  Juniper equipment specific.  This will give you a basic menu and ask you what you want.  1.  Full peers.  2.  Partial (non-established peers) 3. Filtered (Only peers that have changed in the last 24 hours).  It then provides the status of BGP peers per routing-instance.

**vcenter-cluster-info.py**:  Auth's against vCenter.  Put in any part of a name of your VM Cluster - it returns back the Cluster name, host's in the cluster as well as what VLAN tags are on the corresponding host's dvSwitch.