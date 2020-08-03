import requests

token = "Token ..."
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": token
}
NETBOX_API_ROOT_ROOT = "http:netbox.com:8000/api"
NETBOX_DEVICES_ENDPOINT = "/dcim/devices/"
NETBOX_SITES_ENDPOINT = "/dcim/sites/"
NETBOX_IP_ADDRESSES_ENDPOINT = "/ipam/ip-addresses/"


def get_device_ip_info(device_name):
    LOCAL_ENDPOINT = NETBOX_API_ROOT_ROOT + NETBOX_IP_ADDRESSES_ENDPOINT + "?device={}".format(device_name)

    r = requests.get(LOCAL_ENDPOINT, headers=headers)
    ip_address = {}
    for i in r.json()['results']:
        ip_address[i['interface']['name']] = i['address']
    return ip_address


def get_device_info(device_name):
    LOCAL_ENDPOINT = NETBOX_API_ROOT_ROOT + NETBOX_DEVICES_ENDPOINT + "?name={}".format(device_name)

    r = requests.get(LOCAL_ENDPOINT, headers=headers)
    device_info_local = {}
    r = r.json()
    device_info_local['model'] = r['results'][0]["device_type"]['slug']
    device_info_local['role'] = r['results'][0]['device_role']['slug']
    device_info_local['site'] = r['results'][0]['site']['slug']
    return device_info_local
