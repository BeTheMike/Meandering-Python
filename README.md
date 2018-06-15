# Meandering-Python
Trying to catch the development train while laying on the tracks.


#### Some short descriptions on scripts:

**IBlox-IP-Info.py**: Does an API lookup for a hostname or IP (or multiple if you want) against your Infoblox database.
It will give you all the subnet info for the IP as well as ny Network Attributes assigned to it as well as if there are one
or multiple "A" records.

**single-string-cleanup.py**
This will iterate through a directory structure (just text files) looking for whatever string you put in and replace it 
with whatever you want it replaced with.  It will prompt you for the directory.  It will then give you a list of directories
that it found that string in and give you a chance to cancel out of the replace in case something doesn't look right.

**what-rack.py** | _Needs Updates_ |
Pretty specific script.  This will connect to a Juniper device (tested on QFX10k's), look for a specific IP and pull 
back the IP/Mac info and let you know via LLDP what ToR switch that host is connected to.

