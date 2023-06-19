from lxml import etree
import requests
from WepApp import Searchwebservices as SWS
from WepApp import FieldWebService as FWS
InstanceURL = "https://archer.hcl.com/"
RecordClass = "/RSAarcher/WS/record.asmx"


#CreateRecord
def create_record(SessionToken,m_id,field_values):
    try:
        url = InstanceURL + RecordClass
        soap_envelope ="""
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
            <soap12:Body>
                <CreateRecord xmlns="http://archer-tech.com/webservices/">
                    <sessionToken>{}</sessionToken>
                    <moduleId>{}</moduleId>
                    <fieldValues>{}</fieldValues>
                </CreateRecord>
            </soap12:Body>
        </soap12:Envelope>""".format(SessionToken,m_id,field_values)

        headers ={"Content-Type": "application/soap+xml; charset=utf-8"}

        response = requests.post(url, data=soap_envelope, headers=headers)
        print(soap_envelope)
        print(response)
        if response.status_code == 200:
            Rs_content=response.content
            root = etree.fromstring(Rs_content)
            ns = {'ns': 'http://archer-tech.com/webservices/'}
            result = root.xpath("//ns:CreateRecordResult/text()", namespaces=ns)
            create_record_result=result[0]
            return create_record_result
        else:
            return "Error in Creating Record. Status code:"

    except:
        return "Error in code:"


#CreateRecords
def create_multipile_records(SessionToken,m_id,contentRecords):
    try:
        url = InstanceURL + RecordClass
        soap_envelope ="""
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
            <soap12:Body>
                <CreateRecords xmlns="http://archer-tech.com/webservices/">
                <sessionToken>{}</sessionToken>
                <moduleId>{}</moduleId>
                <contentRecords>{}</contentRecords>
                </CreateRecords>
            </soap12:Body>
        </soap12:Envelope>""".format(SessionToken,m_id,contentRecords)

        headers ={"Content-Type": "application/soap+xml; charset=utf-8"}

        response = requests.post(url, data=soap_envelope, headers=headers)
        print("create records Post Response status code",response.status_code)
        if response.status_code == 200:
            Rs_content=response.content
            root = etree.fromstring(Rs_content)
            ns = {'ns': 'http://archer-tech.com/webservices/'}
            result = root.xpath("//ns:CreateRecordsResult/text()", namespaces=ns)
            create_records_result=result[0]
            return create_records_result
        else:
            return "Error in Creating Records. Status code:"

    except:
        return 'An error occurred'




#creating the field values format
def create_field_values(session_token, applicationname, Inst_all_details,type,data):
    searchresultF=SWS.search_records_by_report(session_token, applicationname, Inst_all_details, "Field")
    if type=='sr':
        field_result = """<![CDATA[<fieldValues>"""
    elif type=='Mr':
        field_result="<Record>"

    for k in searchresultF:
        print(k)
        for d in data:
            if k["type"] != "4":
                if k['name'] == d['name']:
                    value = d['value']
                    resl = """<Field id="{}" value="{}"/>""".format(k['id'], value)
                    field_result = field_result + resl
                else:
                    field_result = field_result
            elif k["type"] == "4":
                if k['name'] == d['name']:
                    ivalue = d['value']
                    value = FWS.LookupListValue(session_token, k['id'],ivalue)
                    resl = """<Field id="{}" value="{}"/>""".format(k['id'], value)
                    field_result = field_result + resl
                else:
                    field_result = field_result
            else:
                field_result = field_result

    if type=='sr':
        field_final=field_result+"""</fieldValues>]]>"""
    elif type=='Mr':
        field_final = field_result+"</Record>"
    print(field_final)
    return field_final

#UPDATERECORD
def update_Record(SessionToken,moduleId,ContentId,fieldValues):
    try:
        url = InstanceURL + RecordClass
        soap_envelope ="""
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
            <soap12:Body>
                 <UpdateRecord xmlns="http://archer-tech.com/webservices/">
      <sessionToken>{}</sessionToken>
      <moduleId>{}</moduleId>
      <contentId>{}</contentId>
      <fieldValues>{}</fieldValues>
    </UpdateRecord>
            </soap12:Body>
        </soap12:Envelope>""".format(SessionToken,moduleId,ContentId,fieldValues)
        headers ={"Content-Type": "application/soap+xml; charset=utf-8"}

        response = requests.post(url, data=soap_envelope, headers=headers)
        if response.status_code == 200:
            Rs_content=response.content
            root = etree.fromstring(Rs_content)
            ns = {'ns': 'http://archer-tech.com/webservices/'}
            result = root.xpath("//ns:UpdateRecordResult/text()", namespaces=ns)
            UPR_result=result[0]
            return UPR_result
        else:
            return "Error in Updating the record. Status code:"

    except :
        return "An error occurred"


#DeleteRecord
def Delete_Record(SessionToken,moduleId,ContentId):
    try:
        url = InstanceURL + RecordClass
        soap_envelope ="""
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
            <soap12:Body>
                 <DeleteRecord xmlns="http://archer-tech.com/webservices/">
                 <sessionToken>{}</sessionToken>
                 <moduleId>{}</moduleId>
                 <contentId>{}</contentId>
                 </DeleteRecord>
            </soap12:Body>
        </soap12:Envelope>""".format(SessionToken,moduleId,ContentId)
        headers ={"Content-Type": "application/soap+xml; charset=utf-8"}

        response = requests.post(url, data=soap_envelope, headers=headers)
        if response.status_code == 200:
            Rs_content=response.content
            root = etree.fromstring(Rs_content)
            ns = {'ns': 'http://archer-tech.com/webservices/'}
            result = root.xpath("//ns:DeleteRecordResult/text()", namespaces=ns)
            DR_result=result[0]
            return DR_result
        else:
            return "Error in Deleting the record. Status code:"

    except:
        return "An error occurred:"
