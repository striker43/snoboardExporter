import os
import time
import requests
import json
from contextlib import suppress

print("Started Exporter")
NODES = os.environ.get('NODES_LIST', '').split(',')
ACCOUNT_ID = os.environ.get('ACCOUNT', '')

print(f"Using account_id {ACCOUNT_ID}. Following nodes will be queried:")
print(NODES)

gbl_next_submit = 0

while True:
    results_list = []
    for endpoint in NODES:
        try:
            apiRequest = json.loads(requests.get(
                f'http://{endpoint}/api/sno', timeout=5).text)
            apiRequestSatellite = json.loads(requests.get(
                f'http://{endpoint}/api/sno/satellites', timeout=5).text)
            apiRequestEstimatedPayout = json.loads(requests.get(
                f'http://{endpoint}/api/sno/estimated-payout', timeout=5).text)
            apiRequestPaystubs = json.loads(requests.get(
                f'http://{endpoint}/api/heldamount/paystubs/2018-12/2040-01', timeout=5).text)

            node = {
                "apiRequest": apiRequest,
                "apiRequestSatellite": apiRequestSatellite,
                "apiRequestEstimatedPayout": apiRequestEstimatedPayout,
                "payStubs": apiRequestPaystubs
            }
            results_list.append(node)

        except:
            print(f"ERROR: Could not reach node {endpoint}")

    transfer_object = {
        "accountId": ACCOUNT_ID,
        "timestamp": int(time.time()),
        "nodes": results_list
    }
    try:
        update_call = requests.post(
            'https://snoboard.duckdns.org/nodes/update', data=json.dumps(transfer_object))
        response = json.loads(update_call.text)
        print(response)
        if(response['error'] == True):
            print(response['message'])
        else:
            gbl_next_submit = response['nextUpdate']
    except:
        print('ERROR: Could not reach snoboard server.')

    print(
        f"INFO: Sleeping for {min(1800, abs(gbl_next_submit - time.time()))} seconds")
    time.sleep(min(1800, abs(gbl_next_submit - time.time())))
