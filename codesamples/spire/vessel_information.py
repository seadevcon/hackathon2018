"""
An example code to run live queries on the SPIRE API.
"""

import requests
import json
import time
import os

# SPIRE AIS ENDPOINT
ENDPOINT = 'https://ais.spire.com/vessels'

# FORMAT
FORMAT = 'json'

# YOUR TOKEN
AUTH_TOKEN = os.environ.get('SPIRE_API_TOKEN')
HEADERS = {"Authorization": "Bearer {}".format(AUTH_TOKEN), 'Accept': 'application/%s' % FORMAT}

# Message Processing
def process_messages(messages):
    '''Function that will be used to process data fetched from the API'''
    print(len(messages), 'messages')


def query_data(mmsi):
    print('Start Querying SPIRE Data...')
    request = ENDPOINT + "?fields=decoded&mmsi=%s" \
        % (mmsi)
    prev_since = None

    response = requests.get(request, headers=HEADERS)

    data = response.json()

    try:
        process_messages(data['data'])
    except KeyError as e:
        print("Got a KeyError - Reason: %s" % str(e))
        print(data)
        print("Sleep 10 seconds...")
        time.sleep(10)


if __name__ == '__main__':
    mmsi=244710824
    query_data(mmsi)
