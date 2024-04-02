import requests
import json
from getpass import getpass
from rich import print
from time import sleep

requests.packages.urllib3.disable_warnings()

hosts=["10.1.0.5","10.1.0.6"]
port="443"
username='nathanael'
password=getpass()

token = (
    "Enter your token here!"
)

url = "https://webexapis.com/v1/rooms"
wheaders = {'Authorization': f'Bearer {token}','Content-Type': 'application/json', 'Accept':'application/json'}
get_response = requests.get(url, headers=wheaders).json()['items']
for item in get_response:
    if item['title'] == 'ALERTS':
        room_id=item['id']
web_url='https://webexapis.com/v1/messages'

headers={
    'Content-Type': 'application/yang-data+json',
    'Accept': 'application/yang-data+json',
}
router_id=[]

baseurl=f'https://{host}:{port}/restconf/data/'

for host in hosts:
    auth = requests.auth.HTTPBasicAuth(username, password)
    url=f"{baseurl}Cisco-IOS-XE-ospf-oper:ospf-oper-data/ospf-state/ospf-instance"
    r = requests.request("GET", url, auth=auth, headers=headers, verify=False).json()['Cisco-IOS-XE-ospf-oper:ospf-instance'][0]['router-id']
    router_id.append(r)

while True:
    for host in hosts:
        if host == '10.1.0.5':
            url=f"{baseurl}Cisco-IOS-XE-ospf-oper:ospf-oper-data/ospf-state/ospf-instance=address-family-ipv4,{router_id[0]}/ospf-area=0/ospf-interface=GigabitEthernet1/ospf-neighbor"
        elif host == '10.1.0.5':
            url=f"{baseurl}Cisco-IOS-XE-ospf-oper:ospf-oper-data/ospf-state/ospf-instance=address-family-ipv4,{router_id[1]}/ospf-area=0/ospf-interface=GigabitEthernet1/ospf-neighbor"
        r = requests.request("GET", url, auth=auth, headers=headers, verify=False).json()['Cisco-IOS-XE-ospf-oper:ospf-neighbor'][0]
        if r["state"] == 'ospf-nbr-full':
            print(f"Neighbour {r['neighbor-id']} with IP {r['address']} is [green]UP[/green] on host {host}")
            text=f"Neighbour {r['neighbor-id']} with IP {r['address']} is UP on host {host}"
            body={
                'roomId': room_id,
                'text': text
            }
            r=requests.post(web_url,headers=wheaders,data=json.dumps(body))
        else:
            print(f"Neighbour {r['neighbor-id']} with IP {r['address']} is [red]DOWN[/red] on host {host}")
            text=f"Neighbour {r['neighbor-id']} with IP {r['address']} is DOWN on host {host}"
            body={
                'roomId': room_id,
                'text': text
            }
            r=requests.post(web_url,headers=wheaders,data=json.dumps(body))
    sleep(5)