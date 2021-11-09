import configparser
import requests
import json

config = configparser.ConfigParser()
config.read('grouper.ini')
grouper_client = config['ws']['CLIENT']
grouper_password = config['ws']['PASSWORD']

"""
TOKEN=$(curl -XPOST -d grant_type=client_credentials -d scope=grouper-ws -d client_id=it-hpcs-grouper-prod-oauth2-client -d client_secret=$CLIENT_SECRET https://login.lbl.gov/c2id/token | jq -r '.access_token')
"""

data = {'grant_type': 'client_credentials',
        'scope': 'grouper-ws',
        'client_id': grouper_client,
        'client_secret': grouper_password}
response = requests.post('https://login.lbl.gov/c2id/token', data=data)
print(response.json())

"""
{'access_token': 'eyJraWQiOiJ6N0xmIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJpdC1ocGNzLWdyb3VwZXItcHJvZC1vYXV0aDItY2xpZW50Iiwic2NwIjpbImdyb3VwZXItd3MiXSwiaXNzIjoiaHR0cHM6XC9cL2xvZ2luLmxibC5nb3ZcL2MyaWQiLCJleHAiOjE2MzM3MTMzMzYsImlhdCI6MTYzMzcxMjczNiwiY2lkIjoiaXQtaHBjcy1ncm91cGVyLXByb2Qtb2F1dGgyLWNsaWVudCJ9.C_LDAmm_1YFqMh6h8Smet213-b_BnFKLPwHb39NyPDnExT_Rj8mBSr-zEo6nPcMeOx9gK9F7FphNlofhxvHLD6TBWIz_OJjxJWcLQPoNFbT8OHzWslgWwQy3b2NTGnTpzBwBPCf-DPA7EsUuKe96tnnpJZSkq981rCApsBb5AiCDJ4SnpEGjWWaz0uNsoN1-5iiRMzM2XBCsJC-RQEaBbtT-tsIhBNvgmLVEmVlHkvW-uOO7CufBoX_pCJ2d9diHcCuqSdQXW7SGuL5ISHpC6UMYOD8jQAXsH-LkOc3FjeAVN0qZMG7LtoX9EjA6tz5SEPOKaPJ5ltKibbSqCuSoIQ', 'scope': 'grouper-ws', 'token_type': 'Bearer', 'expires_in': 600}
"""

access_token = response.json()['access_token']

"""
curl --silent -XGET -H "Authorization: Bearer $TOKEN" https://identity.lbl.gov/grouper-ws/servicesRest/v2_4_000/groups/org:Operations:Information%20Technology:app:Google%20Groups:alsacc-announce/members | jq
"""

"""
ASCII encoding
space - %20
:     - %3A
org:Operations:Information Technology:app:Google Groups:alsacc-announce -
org%3AOperations%3AInformation%20Technology%3AHPCS%3Aapp%3AGoogle%20Groups%3Aalsacc-announce
"""

# url_base = 'https://identity.lbl.gov/grouper-ws/servicesRest/json/v2_4_000/groups/org%3AOperations%3AInformation%20Technology%3AHPCS%3Aapp%3AGoogle%20Groups%3A'
url_base = 'https://identity.lbl.gov/grouper-ws/servicesRest/v2_4_000/groups/org%3AOperations%3AInformation%20Technology%3AHPCS%3Aapp%3AGoogle%20Groups%3A'
url = url_base + 'alsacc-announce' + '/members'
my_headers = {'Authorization' : f'Bearer {access_token}'}
response = requests.get(url, headers=my_headers)
print(response.json())

"""
https://identity.lbl.gov/grouper/grouperUi/app/UiV2Main.index?operation=UiV2Subject.viewSubject&subjectId=065536&sourceId=people
"""

url = 'https://identity.lbl.gov/grouper-ws/servicesRest/v2_4_000/subjects/065536'
response = requests.get(url, headers=my_headers)
# print(response.json())
print(response)

url = 'https://identity.lbl.gov/grouper-ws/servicesRest/v2_4_000/subjects/sources/people/subjectId/065536'
response = requests.get(url, headers=my_headers)
# print(response.json())
print(response)

url = 'https://identity.lbl.gov/grouper-ws/servicesRest/v2_4_000/subjects?wsLiteObjectType=WsRestGetSubjectsLiteRequest&subjectId=065536'
response = requests.get(url, headers=my_headers)
# print(response.json())
print(response)

url = 'https://identity.lbl.gov/grouper-ws/servicesRest/v2_4_000/subjects/subjectId/065536'
response = requests.get(url, headers=my_headers)
# print(response.json())
print(response)

url = 'https://identity.lbl.gov/grouper-ws/servicesRest/v2_4_000/subjects/subjectId/065536'
response = requests.get(url, headers=my_headers)
# print(response.json())
print(response)

response = requests.post('https://identity.lbl.gov/grouper-ws/servicesRest/v2_4_000/subjects', headers=my_headers, json={
  "WsRestGetSubjectsLiteRequest":{
    "searchString":"065536"
  }
})
# print(response.json())
print(response)
print(response.json())

response = requests.post('https://identity.lbl.gov/grouper-ws/servicesRest/v2_4_000/subjects', headers=my_headers, json={
  "WsRestGetSubjectsRequest":{
    "wsSubjectLookups":[
      {
        "subjectId":"065536"
      }
    ],
  }
})
# print(response.json())
print(response)
