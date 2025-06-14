import sys
import requests
import json
import logging
import csv


def get_new_token():

    auth_server_url = "AuthenticationURLGoesHere" #Authentication URL Goes Here
    client_id = 'TokenIDGoesHere' #Token ID goes here
    client_secret = 'TokenPasswordGoesHere' #Token password goes here

    token_req_payload = {'grant_type': 'client_credentials'}

    token_response = requests.post(auth_server_url, data=token_req_payload, verify=False, allow_redirects=False, auth=(client_id, client_secret))
                
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
        sys.exit(1)

    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']



logging.captureWarnings(True)
test_api_url = "TestAPIURL" #Test API url goes here

fileData = list(csv.reader(open("DeviceSerials.csv")))
serialList = []
increment = 1


with open("WarrantyInfo.csv", mode="w", newline="") as csvFile:
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["Serial Code", "Warranty Expiration Date", "Coverage Level"])

    for data in fileData:
        serialList.append(data[0])

    listLength = round(len(serialList) / 100, 2)
    if listLength < 1:
        listLength = 1
    

    while listLength >= 1:
        tempList = serialList[0:99]

        for code in tempList:
            if increment == 1:
                test_api_url += code
                increment += 1
            else:
                test_api_url += "," + code

            serialList.remove(code)
 


        token = get_new_token()

        api_call_headers = {'Authorization': 'Bearer ' + token}
        api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)

        if	api_call_response.status_code == 401:
            token = get_new_token()
        else:
            userData = json.loads(api_call_response.text)

        for item in userData:
            serial = item["serviceTag"]
            
            try:
                entitlements = item["entitlements"][1]
            except IndexError:
                entitlements = "Expired"

            try:
                warrantyEnd = entitlements["endDate"][0:10]
            except TypeError:
                warrantyEnd = "Expired"

            try:
                serviceLevel = entitlements["serviceLevelDescription"]
            except TypeError:
                serviceLevel = "No Warranty"

            csvWriter.writerow([serial, warrantyEnd, serviceLevel])

        listLength -= 1
        increment = 1
        tempList = []
        test_api_url = "TestAPIURL" #Test API url goes here
        if listLength > 0 and listLength < 1:
            listLength = 1