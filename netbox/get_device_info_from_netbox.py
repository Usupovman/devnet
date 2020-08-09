import requests
import yaml

'''This module gets info from netbox about device, then  create yaml file in 
directory "/data_yaml" and write information on this file '''

token = "Token ****************************************"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": token
}
NETBOX_API_ROOT_ROOT = "http:********************/api"
NETBOX_DEVICES_ENDPOINT = "/dcim/devices/"
NETBOX_SITES_ENDPOINT = "/dcim/sites/"
NETBOX_IP_ADDRESSES_ENDPOINT = "/ipam/ip-addresses/"


def get_device_info(device_name):
    import ipaddress
    device_info_local = {}

    LOCAL_ENDPOINT = NETBOX_API_ROOT_ROOT + NETBOX_DEVICES_ENDPOINT + "?name={}".format(device_name)

    r = requests.get(LOCAL_ENDPOINT, headers=headers)
    if r.status_code != 200:
        print('something wrong')
        return False

    r = r.json()
    if not r['results']:
        print('wrong name')
        return False

    device_info_local['model'] = r['results'][0]["device_type"]['slug']
    device_info_local['role'] = r['results'][0]['device_role']['slug']
    device_info_local['site'] = r['results'][0]['site']['slug']
    device_info_local['name'] = r['results'][0]['name']

    LOCAL_GET_AREA_ENDPOINT = NETBOX_API_ROOT_ROOT + NETBOX_SITES_ENDPOINT + '?slug={}'.format(
        device_info_local['site'])
    r = requests.get(LOCAL_GET_AREA_ENDPOINT, headers=headers)
    r = r.json()
    device_info_local['area'] = r['results'][0]['custom_fields']['area']

    LOCAL_IP_ADDR_ENDPOINT = NETBOX_API_ROOT_ROOT + NETBOX_IP_ADDRESSES_ENDPOINT + "?device={}".format(device_name)
    r = requests.get(LOCAL_IP_ADDR_ENDPOINT, headers=headers)
    local_intefaces = {}
    for i in r.json()['results']:
        local_intefaces[i['interface']['name']] = i['address']

    interfaces = []
    networks = []
    for i in local_intefaces:
        j = {}
        m = {}
        j['name'] = i
        interface = ipaddress.ip_interface(local_intefaces[i])
        j['address'] = str(interface.ip)
        j['netmask'] = str(interface.netmask)
        net = interface.network
        m['network'] = str(net)
        m['netmask'] = str(net.netmask)
        m['wildmask'] = str(net.hostmask)
        m['network_address'] = str(net.network_address)
        interfaces.append(j)
        networks.append(m)
    device_info_local['interfaces'] = interfaces
    device_info_local['networks'] = networks

    return device_info_local


while True:
    device = input('enter device name: ')
    c = get_device_info(device)
    if not c:
        print('Try Again')
        continue
    with open('data_yaml/' + device + '_info.yaml', 'w') as f:
        yaml.dump(c, f, default_flow_style=False)
        print('Yaml file created success!!!')
        break
