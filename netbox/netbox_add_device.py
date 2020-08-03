import requests
import json

token = "Token ..."
NETBOX_API_ROOT = "http://netbox.com:8000/api"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Token ..."
}

region_end_point = NETBOX_API_ROOT + "/dcim/regions"

table_header = ['id', 'name']


def get_region():
    req = requests.get(region_end_point, headers=headers)
    req_dic = req.json()
    print('Всего регионов: {}'.format(req_dic['count']))
    print("-" * 30)
    print("{}  {}".format('id', 'name'))
    for i in req.json()['results']:
        print("{}   {}".format(i['id'], i['name']))
    local_region_id = input('enter region id: ')
    return local_region_id


def get_sites(arg):
    sites_endpoint = NETBOX_API_ROOT + "/dcim/sites/?region_id={}".format(arg)
    req_sites = requests.get(sites_endpoint, headers=headers)
    req_sites_json = req_sites.json()

    print('-' * 30)
    print("{}  {}".format('id', 'name'))
    for i in req_sites_json['results']:
        print("{}  {}".format(i['id'], i['name']))

    local_site_id = input('Enter site id ')
    return local_site_id


def get_vendor():
    manufacturer_endpoint = NETBOX_API_ROOT + "/dcim/manufacturers/"
    req_man = requests.get(manufacturer_endpoint, headers=headers)
    req_man_json = req_man.json()
    print("-" * 30)
    print("{}  {}".format("id", "vendor name"))
    for i in req_man_json["results"]:
        print("{}  {}".format(i["id"], i["name"]))
    local_man_id = input("Enter vendor id: ")
    return local_man_id


def get_type(arg):
    type_endpoint = NETBOX_API_ROOT + "/dcim/device-types/?manufacturer_id={}".format(arg)
    req_types = requests.get(type_endpoint, headers=headers)
    req_types_json = req_types.json()
    print('-' * 30)
    print("{}  {}".format("id", "name"))
    for i in req_types_json["results"]:
        print("{}  {}".format(i["id"], i["model"]))
    local_model_id = input('Endter model id')
    return local_model_id


def add_device(model, site, name):
    device_endpoint = NETBOX_API_ROOT + "/dcim/devices/"
    payload = {
        "name": name,
        "device_type": int(model),
        "device_role": 1,
        "site": int(site),
        "status": "active"
    }

    req_new_dev = requests.post(
        device_endpoint,
        headers=headers,
        data=json.dumps(payload)
    )
    if req_new_dev.status_code == 201:
        print(f"Device {name} was created successfully")
    else:
        req_new_dev.raise_for_status()


def get_devices():
    get_devices_adnpoint = NETBOX_API_ROOT + "/dcim/devices/"
    req_devices = requests.get(get_devices_adnpoint, headers=headers)
    req_devices_json = req_devices.json()

    for i in req_devices_json['results']:
        print(i["name"])


def get_ipaddress(site):
    get_prefix_endpoint = NETBOX_API_ROOT + "/ipam/prefixes/?site_id={}".format(site)
    req_get_pref = requests.get(get_prefix_endpoint, headers=headers)
    req_get_pref_json = req_get_pref.json()
    pref_id = req_get_pref_json['results'][0]['id']
    get_ip_endpoint = NETBOX_API_ROOT + "/ipam/prefixes/{}/available-ips/".format(pref_id)
    req_ip = requests.post(get_ip_endpoint, headers=headers)
    req_ip_json = req_ip.json()
    ip_addr = req_ip_json['address']

    return ip_addr


def get_inteface_id(name):
    end_point = NETBOX_API_ROOT + "/dcim/interfaces/?device={}&name=vlan100".format(name)
    req_get_int_id = requests.get(end_point, headers=headers)
    req_get_int_id_json = req_get_int_id.json()

    return req_get_int_id_json['results'][0]['id']


def add_ip_address(interface_id, ip_address, name):
    print('adding ip address: {} to device {}'.format(ip_address, name))
    local_end_point = NETBOX_API_ROOT + '/ipam/ip-addresses/'
    local_payload = {
        "address": ip_address,
        "status": "active",
        "interface": interface_id
    }
    post_address = requests.post(
        local_end_point,
        headers=headers,
        data=json.dumps(local_payload)
    )
    if post_address.status_code == 201:
        print(f"address was added successfully")
    else:
        post_address.raise_for_status()


site = get_sites(get_region())
model = get_type(get_vendor())
device_name = input('enter device name: ')
ip_address = get_ipaddress(site)

add_device(model=model, site=site, name=device_name)
interface_id = get_inteface_id(device_name)

add_ip_address(interface_id, ip_address, name=device_name)
