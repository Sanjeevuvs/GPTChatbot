import csv

import GeneralWebservice as GWS
import Searchwebservices as SWS
import Recordwebservices as RWS
import Modulewebservice as MWS
import FieldWebService as FWS
import AccessControlWS as ACWS
from flask import Flask,render_template,request,jsonify,session,redirect,url_for
import requests
import pandas as pd
import openai
from xml.etree import ElementTree as ET
from lxml import etree

import chatapp
import config
app=Flask(__name__)
webapp=Flask(__name__)




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/CreateSessionToken',methods=['POST'])
def CreateSessionToken():
    username=request.form['ArcherUserName']
    instance=request.form['ArcherInstancePIN']
    password=request.form['Archerpassword']
    Sessiontoken=GWS.create_session_token(username,instance,password)
    if Sessiontoken is not None:
        return render_template('session.html',session_token=Sessiontoken,ArcherInstancePIN=instance)
    else:
        return "Error creating Session token."

@app.route('/dashboard',methods=['POST'])
def dashboard():
    session_token=request.form["session_token"]
    ArcherInstancePIN=request.form['ArcherInstancePIN']
    return render_template('session.html',session_token=session_token,ArcherInstancePIN=ArcherInstancePIN)

@app.route('/terminate', methods=['POST'])
def terminate_session():
    session_token=request.form['session_token']
    result=GWS.terminate_session_token(session_token)
    return render_template("TerminateSessionToken.html",result=result)


@app.route('/GetReports',methods=['POST'])
def get_reports():
    ArcherInstancePIN = request.form['ArcherInstancePIN']
    session_token = request.form["session_token"]
    Inst_all_details=SWS.Get_Reports(session_token)
    All_details_Df = pd.DataFrame(Inst_all_details)
    pd.set_option('display.max_rows', All_details_Df.shape[0] + 1)
    All_details_html=All_details_Df.to_html(index=False)
    if All_details_Df is not None:
        return render_template("GetReports.html",re_hd="The Applications and Reoprts of Archer are",html_table=All_details_html,session_token=session_token,ArcherInstancePIN=ArcherInstancePIN)
    else:
        return render_template("session.html",session_token=session_token,ArcherInstancePIN=ArcherInstancePIN)


@app.route('/Search',methods=['POST'])
def search():
    session_token = request.form['session_token']
    ArcherInstancePIN = request.form['ArcherInstancePIN']
    Inst_all_details = SWS.Get_Reports(session_token)
    All_details_Df = pd.DataFrame(Inst_all_details)
    pd.set_option('display.max_rows', All_details_Df.shape[0] + 1)
    Appli_details_html = All_details_Df['Application Name']

    if session_token is not None:
        return render_template('SearchRecords.html',session_token=session_token,ArcherInstancePIN=ArcherInstancePIN,Appli_details_html=Appli_details_html)
    else:
        return "Error in Search."

@app.route('/SearchReoprts',methods=['POST'])
def search_records_by_report():
    session_token=request.form['session_token']
    applicationname=request.form['ApplicationName']
    ArcherInstancePIN = request.form['ArcherInstancePIN']
    Inst_all_details=SWS.Get_Reports(session_token)
    searchresult=SWS.search_records_by_report(session_token,applicationname,Inst_all_details,"Search")
    AllRecords_inhtml = searchresult.to_html(index=False)
    if searchresult is not None:
        return render_template("GetReports.html",re_hd="The record Details of",html_table=AllRecords_inhtml,session_token=session_token,applicationname=applicationname,ArcherInstancePIN=ArcherInstancePIN,Recordsdf=searchresult)
    else:
        return render_template("session.html", session_token=session_token,ArcherInstancePIN=ArcherInstancePIN)


@app.route('/CreateRecord',methods=['POST'])
def create():
    session_token = request.form['session_token']
    applicationname = request.form['ApplicationName']
    ArcherInstancePIN = request.form['ArcherInstancePIN']
    Inst_all_details = SWS.Get_Reports(session_token)
    searchresult = SWS.search_records_by_report(session_token, applicationname, Inst_all_details, "Field")

    valuelists=[]
    for searchresults in searchresult:
        if searchresults['type'] == '4':
            getvaluelist = FWS.GetValueListForField(session_token, searchresults['id'],'gv')
            valuelists.append({'name':searchresults['name'],'list':getvaluelist})

    if session_token is not None:
        return render_template('CreateRecord.html',session_token=session_token,applicationname=applicationname,ArcherInstancePIN=ArcherInstancePIN,Recordsdf=searchresult,valuelists=valuelists)
    else:
        return "Error in create."

@app.route('/CreateNewRecord',methods=['POST'])
def CreateRecord():
    session_token = request.form['session_token']
    applicationname = request.form['applicationname']
    ArcherInstancePIN = request.form['ArcherInstancePIN']
    Inst_all_details = SWS.Get_Reports(session_token)
    searchresult = SWS.search_records_by_report(session_token, applicationname, Inst_all_details, "Field")

    data=[]
    for field in searchresult :
        if field['name'] == 'Tracking ID':
            data=data
        else:
            name = field['name']
            value = request.form[name]
            data.append({'name': name, 'value': value})

    AppGUID = SWS.application_Details_Passing(0, applicationname, Inst_all_details)
    ModuleId = MWS.get_moduleid_by_guid(session_token, ArcherInstancePIN, AppGUID)  # 1324  APPName,APPnum,Discp
    FieldValue = RWS.create_field_values(session_token, applicationname, Inst_all_details, 'sr',data)

    create_record_rs = RWS.create_record(session_token, ModuleId, FieldValue)

    if create_record_rs is not None:
        searchresult = SWS.search_records_by_report(session_token, applicationname, Inst_all_details, "Search")
        AllRecords_inhtml = searchresult.to_html(index=False)
        return render_template("GetReports.html", re_hd="The record Details of", html_table=AllRecords_inhtml,
                               session_token=session_token, applicationname=applicationname,
                               ArcherInstancePIN=ArcherInstancePIN,Recordsdf=searchresult)
    else:
        return render_template("session.html", session_token=session_token, ArcherInstancePIN=ArcherInstancePIN)

@app.route('/CreateMultiRecords',methods=['POST'])
def Upload():
    session_token = request.form['session_token']
    applicationname = request.form['ApplicationName']
    ArcherInstancePIN = request.form['ArcherInstancePIN']
    Inst_all_details = SWS.Get_Reports(session_token)
    searchresult = SWS.search_records_by_report(session_token, applicationname, Inst_all_details, "Field")
    if session_token is not None:
        return render_template('MultipleRecord.html', session_token=session_token, applicationname=applicationname,
                               ArcherInstancePIN=ArcherInstancePIN, Recordsdf=searchresult)
    else:
        return "Error in create."

@app.route('/CreateRecords', methods=['POST'])
def CreateRecords():
    session_token = request.form['session_token']
    applicationname = request.form['ApplicationName']
    ArcherInstancePIN = request.form['ArcherInstancePIN']
    Inst_all_details = SWS.Get_Reports(session_token)
    file = request.files["file"]
    if file:
        filename=file.filename
        file.save(filename)
        df=pd.read_csv(filename)
        list=df.to_dict('records')

    ContentRecord = "<![CDATA[<fieldValues>"
    for i in list:
        data = []
        keys = i.keys()
        for k in keys:
            data.append({'name': k, 'value': i[k]})
        FieldValue = RWS.create_field_values(session_token, applicationname, Inst_all_details, 'Mr', data)
        ContentRecord = ContentRecord + FieldValue

    ContentRecord = ContentRecord+ "</fieldValues>]]>"
    AppGUID = SWS.application_Details_Passing(0, applicationname, Inst_all_details)
    ModuleId = MWS.get_moduleid_by_guid(session_token, ArcherInstancePIN, AppGUID)  # 1324  APPName,APPnum,Discp
    CreateRecordsresult=RWS.create_multipile_records(session_token,ModuleId,ContentRecord)

    if CreateRecordsresult is not None:
        searchresult = SWS.search_records_by_report(session_token, applicationname, Inst_all_details, "Search")
        AllRecords_inhtml = searchresult.to_html(index=False)
        return render_template("GetReports.html", re_hd="The record Details of", html_table=AllRecords_inhtml,
                               session_token=session_token, applicationname=applicationname,
                               ArcherInstancePIN=ArcherInstancePIN, Recordsdf=searchresult)
    else:
        return render_template("session.html", session_token=session_token, ArcherInstancePIN=ArcherInstancePIN)

@app.route("/UpdateRecord",methods=['POST'])
def update():
    session_token = request.form['session_token']
    applicationname = request.form['ApplicationName']
    ArcherInstancePIN = request.form['ArcherInstancePIN']
    Inst_all_details = SWS.Get_Reports(session_token)
    searchresult = SWS.search_records_by_report(session_token, applicationname, Inst_all_details, "Field")
    valuelists = []
    for searchresults in searchresult:
        if searchresults['type'] == '4':
            getvaluelist = FWS.GetValueListForField(session_token, searchresults['id'], 'gv')
            valuelists.append({'name': searchresults['name'], 'list': getvaluelist})
    TrackingID = request.form['TrackingID']
    return render_template("Update Record.html",session_token=session_token,applicationname=applicationname,ArcherInstancePIN=ArcherInstancePIN,Recordsdf=searchresult,TrackingID=TrackingID,valuelists=valuelists)


@app.route("/UpdateTheRecord",methods=['POST'])
def UpdateTheRecord():
    session_token = request.form['session_token']
    applicationname = request.form['ApplicationName']
    ArcherInstancePIN = request.form['ArcherInstancePIN']
    TrackingID=int(request.form['TrackingID'])

    Inst_all_details = SWS.Get_Reports(session_token)
    searchresult = SWS.search_records_by_report(session_token, applicationname, Inst_all_details, "Field")
    data = []
    for field in searchresult:
        if field['name'] == 'Tracking ID':
            data = data
        else:
            name = field['name']
            value = request.form[name]
            data.append({'name': name, 'value': value})

    AppGUID = SWS.application_Details_Passing(0, applicationname, Inst_all_details)
    ModuleId = MWS.get_moduleid_by_guid(session_token, ArcherInstancePIN, AppGUID)  # 1324  APPName,APPnum,Discp
    FieldValue = RWS.create_field_values(session_token, applicationname, Inst_all_details, 'sr', data)

    UpdateRecordResult = RWS.update_Record(session_token, ModuleId,TrackingID, FieldValue)

    if UpdateRecordResult is not None:
        searchresult = SWS.search_records_by_report(session_token, applicationname, Inst_all_details, "Search")
        AllRecords_inhtml = searchresult.to_html(index=False)
        return render_template("GetReports.html", re_hd="The Updated Record Details of", html_table=AllRecords_inhtml,
                               session_token=session_token, applicationname=applicationname,
                               ArcherInstancePIN=ArcherInstancePIN, Recordsdf=searchresult)
    else:
        return render_template("session.html", session_token=session_token, ArcherInstancePIN=ArcherInstancePIN)


@app.route('/DeleteRecord',methods=['POST'])
def DeleteRecord():
    session_token = request.form['session_token']
    applicationname = request.form['ApplicationName']
    ArcherInstancePIN = request.form['ArcherInstancePIN']
    Inst_all_details = SWS.Get_Reports(session_token)
    AppGUID = SWS.application_Details_Passing(0, applicationname, Inst_all_details)
    ModuleId = MWS.get_moduleid_by_guid(session_token, ArcherInstancePIN, AppGUID)
    TrackingID = request.form['TrackingID']
    deleteresult=RWS.Delete_Record(session_token, ModuleId, TrackingID)
    if deleteresult is not None:
        searchresult = SWS.search_records_by_report(session_token, applicationname, Inst_all_details, "Search")
        AllRecords_inhtml = searchresult.to_html(index=False)
        return render_template("GetReports.html", re_hd="After deleting, The Record Details of ", html_table=AllRecords_inhtml,
                               session_token=session_token, applicationname=applicationname,
                               ArcherInstancePIN=ArcherInstancePIN, Recordsdf=searchresult)
    else:
        return render_template("session.html", session_token=session_token, ArcherInstancePIN=ArcherInstancePIN)

@app.route('/AccessControl',methods=['POST'])
def accesscontrol():
    session_token = request.form['session_token']
    ArcherInstancePIN = request.form['ArcherInstancePIN']
    Inst_all_details = SWS.Get_Reports(session_token)
    if session_token is not None:
        return render_template('AccessControl.html',session_token=session_token,ArcherInstancePIN=ArcherInstancePIN)
    else:
        return "Error Access Control"

@app.route('/GetUserList',methods=['POST'])
def getuserlist():
    session_token = request.form['session_token']
    ArcherInstancePIN = request.form['ArcherInstancePIN']
    Inst_all_details = SWS.Get_Reports(session_token)

    UsersList=ACWS.GetUserList(session_token)
    UsersListhtml = UsersList.to_html(index=False)

    if UsersList is not None:
        return render_template('ResultScreen.html',re_hd="The Users List in Archer is ", html_table=UsersListhtml,session_token=session_token,ArcherInstancePIN=ArcherInstancePIN)
    else:
        return "Error getting userlist token."


def page_not_found(e):
    return render_template('404.html'), 404
app.config.from_object(config.config['development'])

app.register_error_handler(404, page_not_found)

@app.route('/Gptindex.html',methods=['POST','GET'])
def chatting():
    if request.method=="POST":
        prompt = request.form['prompt']
        answer = chatapp.generateChatResponse(prompt)
        print("Question : \n", prompt)
        print("Response :")
        print(answer)
        res = {}
        res['answer'] = answer.choices[0].text.strip().replace('\n', '<br>')

        return jsonify(res), 200
    return render_template('Gptindex.html', **locals())





if __name__=='__main__':
    app.run(debug=True)

    #app.run(host='0.0.0.0',port='90890',debug=True)
