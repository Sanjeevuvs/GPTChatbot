from xml.etree import ElementTree as ET
from lxml import etree
import pandas as pd
import requests

#GeneralClass
InstanceURL = "https://archer.hcl.com/"
GeneralClass = "/RSAarcher/WS/General.asmx"
#creating the User Session from instance
def create_session_token(archerusername, archerinstancepin, archerpassword):
    try:
        url = InstanceURL + GeneralClass
        soap_envelope = """
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
            <soap12:Body>                
                <CreateUserSessionFromInstance xmlns="http://archer-tech.com/webservices/">                    
                    <userName>{}</userName>                    
                    <instanceName>{}</instanceName>                    
                    <password>{}</password>                
                </CreateUserSessionFromInstance>            
            </soap12:Body>
        </soap12:Envelope>""".format(archerusername, archerinstancepin, archerpassword)
        headers = {"Content-Type": "application/soap+xml; charset=utf-8"}
        response = requests.post(url, data=soap_envelope, headers=headers)
        if response.status_code == 200:
            Rs_content = response.content
            root = etree.fromstring(Rs_content)
            ns = {'ns': 'http://archer-tech.com/webservices/'}
            result = root.xpath("//ns:CreateUserSessionFromInstanceResult/text()", namespaces=ns)
            SessionToken = result[0]

        else:
            SessionToken=None
    except:
        SessionToken = None
    return SessionToken

#Terminating the Session
def terminate_session_token(SessionToken):
    try:
        url = InstanceURL + GeneralClass
        soap_envelope ="""
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
            <soap12:Body>
                <TerminateSession xmlns="http://archer-tech.com/webservices/">
                    <sessionToken>{}</sessionToken>
                </TerminateSession>
            </soap12:Body>
        </soap12:Envelope>""".format(SessionToken)
        headers ={"Content-Type": "application/soap+xml; charset=utf-8"}

        response = requests.post(url, data=soap_envelope, headers=headers)
        if response.status_code == 200:
            return "Session Terminated Successfully"
        else:
            return "Error in Terminating the session. Status code:"

    except:
        return "An error occurred"


