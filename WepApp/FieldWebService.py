from lxml import etree
import requests
from xml.etree import ElementTree as ET
InstanceURL = "https://archer.hcl.com/"
FieldClass = "/RSAarcher/WS/field.asmx"

#getvaluelistfor field
def GetValueListForField(SessionToken,field_id,ty):
    try:
        url = InstanceURL + FieldClass
        soap_envelope ="""<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <GetValueListForField xmlns="http://archer-tech.com/webservices/">
      <sessionToken>{}</sessionToken>
      <fieldId>{}</fieldId>
    </GetValueListForField>
  </soap12:Body>
</soap12:Envelope>""".format(SessionToken,field_id)
        headers ={"Content-Type": "application/soap+xml; charset=utf-8"}

        response = requests.post(url, data=soap_envelope, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            Rs_content=response.content

            root = etree.fromstring(Rs_content)
            ns = {'ns': 'http://archer-tech.com/webservices/'}
            result = root.xpath("//ns:GetValueListForFieldResult/text()", namespaces=ns)
            UPR_result=result[0]
            value_root = ET.fromstring(UPR_result)
            list_definition = value_root.find("SelectDefValues")

            allvaluelist = []
            namevaluelist=[]
            for vl in list_definition:
                dict = {}
                for dv in vl:
                    if dv.tag=='Name':
                        namevaluelist.append(dv.text)
                    dict[dv.tag] = dv.text
                allvaluelist.append(dict)
            if ty=='gv':
                return namevaluelist
            elif ty=='av':
                return allvaluelist
        else:
            return "Error in getvaluelist. Status code:"
    except:
        return 'An error occurred: {e}'

#LookupListValue
def LookupListValue(SessionToken,field_id,inputval):
    try:
        url = InstanceURL + FieldClass
        soap_envelope ="""<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <LookupListValue xmlns="http://archer-tech.com/webservices/">

<sessionToken>{}</sessionToken>

<fieldId>{}</fieldId>

<keyword>{}</keyword>

</LookupListValue>
  </soap12:Body>
</soap12:Envelope>""".format(SessionToken,field_id,inputval)
        headers ={"Content-Type": "application/soap+xml; charset=utf-8"}
        response = requests.post(url, data=soap_envelope, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            Rs_content=response.content

            root = etree.fromstring(Rs_content)
            ns = {'ns': 'http://archer-tech.com/webservices/'}
            result = root.xpath("//ns:LookupListValueResult/text()", namespaces=ns)
            LUVR_result=result[0]
            return LUVR_result
        else:
           return "Error in Terminating the session. Status code:"

    except:
        return 'An error occurred: {e}'
