"""
An example code to run historical queries on the SPIRE API.
"""

import requests
import json
import time
import os

# SPIRE AIS ENDPOINT
ENDPOINT = 'https://ais.spire.com/messages'

# FORMAT
FORMAT = 'json'

# YOUR TOKEN
AUTH_TOKEN = os.environ.get('SPIRE_API_TOKEN')
HEADERS = {"Authorization": "Bearer {}".format(AUTH_TOKEN), 'Accept': 'application/%s' % FORMAT}


# Message Processing
def process_messages(messages):
    '''Function that will be used to process data fetched from the API'''
    print(len(messages), 'messages')


def query_data(received_after, received_before):
    print("Start Querying SPIRE Data...")
    request = ENDPOINT + "?fields=decoded&received_after=%s&received_before=%s" \
        % (received_after, received_before)

    while True:
        print(request)
        response = requests.get(request, headers=HEADERS)

        data = response.json()

        try:
            process_messages(data['data'])
        except KeyError as e:
            print("Got a KeyError - Reason: %s" % str(e))
            print(data)
            print("Sleep 10 seconds...")
            time.sleep(10)
            continue

        try:
            if 'paging' in data:
                print(data['paging'])
                after = data['paging']['after']
                before = data['paging']['before']
                request = ENDPOINT + "?fields=decoded&after=%s&before=%s" % (after, before) # (before, after) #
        except KeyError:
            print('The data transfer is over. Thank you.')
            return


if __name__ == '__main__':
    received_after = "2018-08-05T00:00:00"
    received_before = "2018-08-05T06:10:05"
    query_data(received_after, received_before)
