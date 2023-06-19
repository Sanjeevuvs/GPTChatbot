from xml.etree import ElementTree as ET
from lxml import etree
import pandas as pd
import requests


InstanceURL = "https://archer.hcl.com/"
SearchClass = "/RSAarcher/WS/search.asmx"
#GetReports
def Get_Reports(SessionToken):
    try:
        url = InstanceURL + SearchClass
        soap_envelope = """
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
            <soap12:Body>
            <GetReports xmlns="http://archer-tech.com/webservices/">
            <sessionToken>{}</sessionToken>
            </GetReports>       
            </soap12:Body>
        </soap12:Envelope>""".format(SessionToken)
        headers = {"Content-Type": "application/soap+xml; charset=utf-8"}


        response = requests.post(url, data=soap_envelope, headers=headers)
        if response.status_code == 200:
            Rs_content = response.content
            root = etree.fromstring(Rs_content)
            ns = {'ns': 'http://archer-tech.com/webservices/'}
            result = root.xpath("//ns:GetReportsResult/text()", namespaces=ns)
            Report_result=result[0]

            Report_details = []
            Report_root = ET.fromstring(Report_result)
            for report in Report_root.iter('ReportValue'):
                report_dict = {
                    'Application Name': report.find('ApplicationName').text,
                    'ApplicationGUID': report.find('ApplicationGUID').text,
                    'Report Name': report.find('ReportName').text,
                    'Report Description': report.find('ReportDescription').text,
                    'ReportGUID': report.find('ReportGUID').text
                }
                Report_details.append(report_dict)
        else:
            Report_details=None
    except:
        Report_details=None

    return Report_details

#SearchRecordsByReportId
def search_records_by_report(SessionToken,applicationname,Inst_all_details,TYM):
    try:
        url = InstanceURL + SearchClass
        appli_name = applicationname
        report_id= application_Details_Passing(1,appli_name,Inst_all_details) #{31AA4ECA-BFFA-4C34-AB84-D16D7CAB6778}
        pgno=1 #input("Enter the Page number:") #1
        soap_envelope ="""
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
            <soap12:Body>
            <SearchRecordsByReport xmlns="http://archer-tech.com/webservices/">
            <sessionToken>{}</sessionToken>
            <reportIdOrGuid>{}</reportIdOrGuid>
            <pageNumber>{}</pageNumber>
            </SearchRecordsByReport>
            </soap12:Body>
        </soap12:Envelope>""".format(SessionToken,report_id,pgno)

        headers ={"Content-Type": "application/soap+xml; charset=utf-8"}

        response = requests.post(url, data=soap_envelope, headers=headers)

        if response.status_code == 200:
            Rs_content=response.content
            root = etree.fromstring(Rs_content)
            ns = {'ns': 'http://archer-tech.com/webservices/'}
            result = root.xpath("//ns:SearchRecordsByReportResult/text()", namespaces=ns)
            search_records_by_report_result=result[0]



            '''field_root = ET.fromstring(search_records_by_report_result)
            Record_definition = field_root.find("Record")
            Metadata_definition = field_root.find("Metadata")
            AllRecords = field_root.findall("Record")
            fields_details = []
            
            for Metadata in Metadata_definition:
                for fieldDefinition in Metadata:
                    field_id = fieldDefinition.attrib['id']
                    field_name = fieldDefinition.attrib['name']
                    field_Guid = fieldDefinition.attrib['guid']
                    fields_details.append({'Field_id': field_id, 'Field_name': field_name,'Field_Giud':field_Guid})

            for record in Record_definition:
                for field in fields_details:
                    if record.attrib['id'] == field['Field_id']:
                        field['Field_type'] = record.attrib['type']

            AllRecords_list=[]
            for e_record in AllRecords:
                E_Record={}
                for data in e_record:
                    for field in fields_details:
                        if data.attrib['id']==field['Field_id']:
                            E_Record[field['Field_name']]=data.text
                AllRecords_list.append(E_Record)'''

            str = ET.fromstring(search_records_by_report_result)
            Record_definition = str.findall("Record")
            Metadata_definition = str.find("Metadata")
            fields_details = []
            for Metadata in Metadata_definition:
                for fieldDefinition in Metadata:
                    fields_details.append(fieldDefinition.attrib)

            AllRecords_list = []
            for record in Record_definition:
                E_Record = {}
                for field in record:
                    for fd in fields_details:
                        if field.attrib['id'] == fd['id'] and field.attrib['guid'] == fd['guid']:
                            fd.update(field.attrib)
                            if fd['type'] == '4':
                                for lvs in field:
                                    for LV in lvs:
                                        E_Record[fd['name']] = LV.attrib['displayName']
                            else:
                                E_Record[fd['name']] = field.text
                AllRecords_list.append(E_Record)

            AllRecords_dataframe=pd.DataFrame(AllRecords_list)
            if TYM=="Search":
                return AllRecords_dataframe
            elif TYM=="Field":
                return fields_details
        else:
            return "Error in Search Record. Status code:"
    except:
        return "Null"


#ApplicationDetailsPassing
def application_Details_Passing(ch,application_name,instancealldetails):
    if ch==0:
        for detail in instancealldetails:
            if detail['Application Name'].__contains__(application_name) or detail['Application Name']==application_name :
                rn_result=detail['ApplicationGUID']
    elif ch==1:
        for detail in instancealldetails:
            if detail['Application Name'].__contains__(application_name) or detail['Application Name']==application_name :
                rn_result=detail['ReportGUID']
    return rn_result