import requests
import json
from sys import argv
from getpass import getpass

requests.packages.urllib3.disable_warnings()

host="10.1.0.6"
port="443"
username='nathanael'
if len(argv) == 2:
    password=getpass()
else:
    password = ''

baseurl=f'https://{host}:{port}/restconf/data/'

auth = requests.auth.HTTPBasicAuth(username, password)

headers={
    'Content-Type': 'application/yang-data+json',
    'Accept': 'application/yang-data+json',
}

def restconf_read (url):
    r = requests.request("GET", url, auth=auth, headers=headers, verify=False)
    print(f"GET result code: {r.status_code}")
    if r.status_code >= 400:
        print(f">>Error: {r.text}")
    else:
        print(r.text)

def restconf_write (url, method, write_data):
    r = requests.request(method, url,
        auth=auth, headers=headers, data=json.dumps(write_data), verify=False)
    print(f"Write ({method}) result code: {r.status_code}")
    if r.status_code >= 400:
        print(f">>Error: {r.text}")

def restconf_delete (url):
    r = requests.request("DELETE",url,auth=auth,headers=headers,verify=False)
    print(f"DELETE result code: {r.status_code}")
    if r.status_code >= 400:
        print(f">>Error: {r.text}")

if __name__ == "__main__":
    if len(argv) == 2:
        if argv[1] == 'get_banner':
            url=f'{baseurl}Cisco-IOS-XE-native:native/banner/login/banner/'
            restconf_read(url)
        elif argv[1] == 'set_banner':
            url=f'{baseurl}Cisco-IOS-XE-native:native/banner/login/'
            banner = {'banner':'Dit is R1 voor de I-share kennissessie.'}
            restconf_write(url, method='POST',write_data=banner)
        elif argv[1] == 'del_banner':
            url=f'{baseurl}Cisco-IOS-XE-native:native/banner/login/banner/'
            restconf_delete(url)
        elif argv[1] == 'get_ospf':
            url=f"{baseurl}Cisco-IOS-XE-native:native/interface/Loopback=0"
            restconf_read(url)
            url=f"{baseurl}Cisco-IOS-XE-native:native/router/"
            restconf_read(url)
        elif argv[1] == 'set_ospf':
            url=f"{baseurl}Cisco-IOS-XE-native:native/interface/"
            data={
                "Cisco-IOS-XE-native:Loopback": {
                    "name": 0,
                    "ip": {
                        "address": {
                            "primary": {
                                "address": "20.20.20.1",
                                "mask": "255.255.255.0"
                            }
                        }
                    }
                }
            }
            restconf_write(url, method='POST',write_data=data)
            url=f"{baseurl}Cisco-IOS-XE-native:native/router/"
            data={
                "Cisco-IOS-XE-native:router": {
                    "Cisco-IOS-XE-ospf:router-ospf": {
                        "ospf": {
                            "process-id": [
                                {
                                    "id": 101,
                                    "neighbor": [
                                        {
                                            "ip": "10.1.0.5"
                                        }
                                    ],
								    "router-id": "2.2.2.2",
                                    "network": [
                                        {
                                            "ip": "10.1.0.0",
                                            "wildcard": "0.0.0.255",
                                            "area": 0
                                        },
                                        {
                                            "ip": "20.20.20.0",
                                            "wildcard": "0.0.0.255",
                                            "area": 2
                                        }
                                    ],
                                    "passive-interface":{
                                        "default": False,
                                        "interface": ["GigabitEthernet1"]
                                    }
                                }
                            ]
                        }
                    }
                }
            }
            restconf_write(url, method='PATCH',write_data=data)
            url=f"{baseurl}Cisco-IOS-XE-native:native/interface/GigabitEthernet=1/ip/Cisco-IOS-XE-ospf:router-ospf/"
            data={
                "Cisco-IOS-XE-ospf:router-ospf": {
                    "ospf": {
                        "network": {
                            "non-broadcast": [None]
                        }
                    }
                }
            }
            restconf_write(url, method='PATCH',write_data=data)
        elif argv[1] == 'del_ospf':
            url=f"{baseurl}Cisco-IOS-XE-native:native/interface/Loopback=0"
            restconf_delete(url)
            url=f"{baseurl}Cisco-IOS-XE-native:native/router/router-ospf/ospf"
            restconf_delete(url)
            url=f"{baseurl}Cisco-IOS-XE-native:native/interface/GigabitEthernet=1/"
            data={
                "Cisco-IOS-XE-native:GigabitEthernet": {
                    "name": "1",
                    "ip": {
                        "address": {
                            "dhcp": {
                            }
                        },
                        "Cisco-IOS-XE-nat:nat": {
                            "outside": [None]
                        }
                    },
                    "mop": {
                        "enabled": False,
                        "sysid": False
                    },
                    "Cisco-IOS-XE-ethernet:negotiation": {
                        "auto": True
                    }
                }
            }
            restconf_write(url, method='PUT',write_data=data)
        else:
            print('Prutser!')    
    else:
        print('Prutser!')