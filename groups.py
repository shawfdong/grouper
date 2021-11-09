import configparser
import requests
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

url = 'https://identity.lbl.gov/grouper-ws/servicesRest/v2_4_000/groups'
my_headers = {'Authorization' : f'Bearer {access_token}'}

# for g in ('alsacc', 'baldur', 'catamount', 'cortex', 'dirac1',
for g in ('cortex', 'dirac1',
          'jbei', 'jcap', 'lawrencium', 'math', 'nano', 
          'savio', 'smfarm', 'snowbear', 'vector', 'vulcan'):
    print(f'{g}...')

    add_member_request = {
        "replaceAllExisting": "T",
        "wsGroupLookup": {
            "groupName": f"org:Operations:Information Technology:HPCS:app:Google Groups:{g}-announce"
        }
    }   

    subject_lookups = []

    with open(f'{g}-announce.txt', 'r') as f:
        for line in f:
            email = line.strip()
            if email[-8:] == '@lbl.gov':
                subject_lookups.append({'subjectIdentifier': email, 'subjectSourceId': 'people'})
            else:
                subject_lookups.append({'subjectIdentifier': email, 'subjectSourceId': 'hpcs'})

    add_member_request["subjectLookups"] = subject_lookups
    rest_request = {"WsRestAddMemberRequest": add_member_request}
    response = requests.put(url, headers=my_headers, json=rest_request)
    print(response)
    
    if response.status_code == 500:
        res = response.json()
        add_member_request = {
            "replaceAllExisting": "F",
            "wsGroupLookup": {
                "groupName": f"org:Operations:Information Technology:HPCS:app:Google Groups:{g}-announce"
            }
        }

        subject_lookups = []

        for result in res['WsAddMemberResults']['results']:
            if result['resultMetadata']['success'] == 'F':
                email = result['wsSubject']['id']
                subject_lookups.append({'subjectIdentifier': email, 'subjectSourceId': 'external-email'})

        add_member_request["subjectLookups"] = subject_lookups
        rest_request = {"WsRestAddMemberRequest": add_member_request}

        response = requests.put(url, headers=my_headers, json=rest_request)
        print(response)

        if response.status_code == 500:
            print("Found no source for the following emails:")
            res = response.json()
            for result in res['WsAddMemberResults']['results']:
                if result['resultMetadata']['success'] == 'F':
                    email = result['wsSubject']['id']
                    print(email)
