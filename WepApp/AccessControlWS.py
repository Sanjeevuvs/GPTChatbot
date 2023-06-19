from lxml import etree
from xml.etree import ElementTree as ET
import requests
import pandas as pd
InstanceURL = "https://archer.hcl.com/"
AccessControlClass = "/RSAarcher/WS/accesscontrol.asmx"


#GetUserList
def GetUserList(session_token):
    try:
        url = InstanceURL + AccessControlClass
        soap_envelope ="""
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
            <soap12:Body>
                <GetUserList xmlns="http://archer-tech.com/webservices/">
                <sessionToken>{}</sessionToken>
                </GetUserList>
            </soap12:Body>
        </soap12:Envelope>""".format(session_token)

        headers ={"Content-Type": "application/soap+xml; charset=utf-8"}

        response = requests.post(url, data=soap_envelope, headers=headers)

        if response.status_code == 200:
            Rs_content=response.content
            root = etree.fromstring(Rs_content)
            ns = {'ns': 'http://archer-tech.com/webservices/'}
            result = root.xpath("//ns:GetUserListResult/text()", namespaces=ns)
            GetUserListResult=result[0]

            user_root = ET.fromstring(GetUserListResult)
            user_definition = user_root.findall("User")

            userlist = []
            for user_def in user_definition:
                dict = {}
                for user in user_def:
                    dict[user.tag] = user.text
                userlist.append(dict)
            usersList_df = pd.DataFrame(userlist)

            return usersList_df
        else:
            return "Error in getting userlist. Status code:"

    except:
        return "Error in getting userlist. Status code:"
