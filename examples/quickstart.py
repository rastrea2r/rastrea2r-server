
import requests
import json

user = 'testuser'
passwd = 'testpass'
url = 'http://localhost:5000'

# Make a request 
r = requests.get(url + '/rastrea2r/api/v1.0/info?var=testvar', auth=(user, passwd), verify=False)

# Check for proper response
if r.status_code == 200:

    # JSON Dict
    response = r.json()

    # Dump JSON in pretty format
    print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))
else:
    print("Request Error:", r.status_code, r.text)

