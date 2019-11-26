import json
import getpass
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable that stupid HTTPS warning ... for now
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Converts the 1 to 4 digit number from Infoblox to a percentage.
# i.e '882' is really 88.2%
def NumberConvert(number):
    num_length = len(str(number))
    num_as_string = str(number)
    if num_length < 3:
        pass
    elif number >= 600:
        print(f"Network: {net} - Utilization: {num_as_string[:-1]}%".center(25))


# User Info
user = input("Enger Infoblox Username: ")
password = getpass.getpass("\nEnter Infoblox Password: ")
print("")

api_url_dhcp = requests.get("https://<Infoblox-IP>/wapi/v2.10/range", verify=False, auth=(user, password))
dhcp_range_data = json.loads(api_url_dhcp.text)

# Build list of all DHCP scope _ref's and their network.
dhcp_ref_list = []
dhcp_network_list = []
dhcp_ref_dict = {}
for dhcp_record in dhcp_range_data:
    dhcp_network_list.append(dhcp_record['network'])

for n in dhcp_network_list:
    for s in dhcp_range_data:
        if n == s['network']:
            dhcp_ref_dict[n] = s['_ref']

for net, ref in dhcp_ref_dict.items():
    dhcp_param = {
        '_return_fields': 'dhcp_utilization,total_hosts,dynamic_hosts,static_hosts', 'statistics_object': ref
    }

    scope_info = requests.get('https://<Infoblox-IP>/wapi/v2.10/dhcp:statistics', params=dhcp_param,
                              verify=False, auth=(user, password))
    scope_info_text = json.loads(scope_info.text)

    NumberConvert(scope_info_text['dhcp_utilization'])

print("")