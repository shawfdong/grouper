import configparser
import requests
from ldap3 import Server, Connection
import json

config = configparser.ConfigParser()
config.read('grouper.ini')
grouper_client = config['ws']['CLIENT']
grouper_password = config['ws']['PASSWORD']

data = {'grant_type': 'client_credentials',
        'scope': 'grouper-ws',
        'client_id': grouper_client,
        'client_secret': grouper_password}
response = requests.post('https://login.lbl.gov/c2id/token', data=data)
access_token = response.json()['access_token']

ldap_host = "ldaps://identity.lbl.gov"
server = Server(ldap_host)
conn = Connection(server, auto_bind=True)
search_base1 = 'ou=people,dc=lbl,dc=gov'

for g in ('alsacc', 'baldur', 'catamount', 'cortex', 'dirac1',
          'jbei', 'jcap', 'lawrencium', 'math', 'nano', 'savio', 
          'smfarm', 'snowbear', 'vector', 'vulcan'):
    print(f'{g}-announce_managers...')
    add_member_request = {
        "replaceAllExisting": "F",
        "wsGroupLookup": {
            "groupName": f"org:Operations:Information Technology:HPCS:app:Google Groups:{g}-announce_managers"
        }   
    }

    subject_lookups = []
    for i in ("065536", "058460", "022339", "023699", "033635", "065637"):
        subject_lookups.append({"subjectIdentifier": i})

    add_member_request["subjectLookups"] = subject_lookups
    rest_request = {"WsRestAddMemberRequest": add_member_request}

    url = 'https://identity.lbl.gov/grouper-ws/servicesRest/v2_4_000/groups'
    my_headers = {'Authorization' : f'Bearer {access_token}'}
    response = requests.put(url, headers=my_headers, json=rest_request)
    print(response)
