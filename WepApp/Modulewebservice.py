import requests
from lxml import etree

InstanceURL = "https://archer.hcl.com/"
ModuleClass = "/RSAarcher/WS/module.asmx"

#GetModuleIdByGuid
def get_moduleid_by_guid(SessionToken,ArcherInstancePIN,AppGUID):
    try:
        url = InstanceURL + ModuleClass
        soap_envelope ="""
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
            <soap12:Body>
                <GetModuleIdByGUID xmlns="http://archer-tech.com/webservices/">
                <sessionToken>{}</sessionToken>
                <instanceId>{}</instanceId>
                <GUID>{}</GUID>
                </GetModuleIdByGUID>
            </soap12:Body>
        </soap12:Envelope>""".format(SessionToken,ArcherInstancePIN,AppGUID)
        headers ={"Content-Type": "application/soap+xml; charset=utf-8"}

        response = requests.post(url, data=soap_envelope, headers=headers)

        if response.status_code == 200:
            Rs_content=response.content
            root = etree.fromstring(Rs_content)
            ns = {'ns': 'http://archer-tech.com/webservices/'}
            result = root.xpath("//ns:GetModuleIdByGUIDResult/text()", namespaces=ns)
            moduleId_result=result[0]
            return moduleId_result
        else:
            return "Error in Getting Module Id. Status code:"

    except:
       return "Error in Getting Module Id. Status code:"
