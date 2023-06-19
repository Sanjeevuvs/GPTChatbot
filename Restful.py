import requests
import json


def get_session_token():
    url = " http://RsaArcher/platformapi/core/security/login"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8"
    }
    payload = {
        "InstanceName": "v5.0",
        "Username": "myuser",
        "UserDomain": "HCLTraining",
        "Password": "Sanuvs@143"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["Token"]
    else:
        return None


print(get_session_token())
