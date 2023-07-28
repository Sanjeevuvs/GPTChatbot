from WepApp import GeneralWebservice as GWS
from WepApp import Recordwebservices as RWS
from WepApp import Searchwebservices as SWS
from WepApp import FieldWebService as FWS
from WepApp import Modulewebservice as MWS
import pandas as pd


username="
instance="
password="

def CreateSessionToken():
    username="
    instance=g"
    password="S
    Sessiontoken=GWS.create_session_token(username,instance,password)
    return Sessiontoken

def CreateRecord(RData,applicationname):
    session_token=CreateSessionToken()
    ArcherInstancePIN = instance

    Inst_all_details = SWS.Get_Reports(session_token)
    searchresult = SWS.search_records_by_report(session_token, applicationname, Inst_all_details, "Field")

    data = []
    for key in RData.keys():
        data.append({'name': key, 'value': RData[key]})
    print(data)
    AppGUID = SWS.application_Details_Passing(0, applicationname, Inst_all_details)
    ModuleId = MWS.get_moduleid_by_guid(session_token, ArcherInstancePIN, AppGUID)  # 1324  APPName,APPnum,Discp
    FieldValue = RWS.create_field_values(session_token, applicationname, Inst_all_details, 'sr', data)

    create_record_rs = RWS.create_record(session_token, ModuleId, FieldValue)
    return create_record_rs

def create(applicationname):
    session_token = CreateSessionToken()
    ArcherInstancePIN = instance
    Inst_all_details = SWS.Get_Reports(session_token)
    searchresult = SWS.search_records_by_report(session_token, applicationname, Inst_all_details, "Field")

    valuelists=[]
    for searchresults in searchresult:
        if searchresults['type'] == '4':
            getvaluelist = FWS.GetValueListForField(session_token, searchresults['id'],'gv')
            valuelists.append({'name':searchresults['name'],'list':getvaluelist})

    details={"searchresult":searchresult,"valuelist":valuelists}
    print(valuelists)
    print(searchresult)
    return details

def applidetails():
    session_token = CreateSessionToken()
    Inst_all_details = SWS.Get_Reports(session_token)
    All_details_Df = pd.DataFrame(Inst_all_details)
    pd.set_option('display.max_rows', All_details_Df.shape[0] + 1)
    Appli_details = All_details_Df['Application Name']
    return Appli_details
