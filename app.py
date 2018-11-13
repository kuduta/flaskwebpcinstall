"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""


import json
import pandas as pd
from datetime import datetime,timedelta
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine ,func


app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.

wsgi_app = app.wsgi_app
engine = create_engine('postgresql://postgres:P@ssw0rd308@localhost/pcinstall',echo=False)


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:P@ssw0rd308@localhost/pcinstall'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = "cominfo"
    id = db.Column(db.Integer, primary_key=True)
    comName_ = db.Column(db.String(30))
    serialNumber_ = db.Column(db.String(50))
    SID_ = db.Column(db.String(200))
    manufacturer_ = db.Column(db.String(100))
    ntVer_ = db.Column(db.String(5))
    operSys_ = db.Column(db.String(200))
    domain_ = db.Column(db.String(100))
    ipaddress_ = db.Column(db.String(16))
    netID_ = db.Column(db.String(16))
    MAC_ = db.Column(db.String(30))
    productName_ = db.Column(db.String(100))
    version_ = db.Column(db.String(5))
    GUID_ = db.Column(db.String(100))
    server_ = db.Column(db.String(16))
    inputTime_= db.Column(db.String(20))
    inputDate_ = db.Column(db.String(20))
    ioffCode_ = db.Column(db.String(20))
    ioffName_ = db.Column(db.String(50))
    iinPak_ = db.Column(db.String(2))
    iinProvince_ = db.Column(db.String(16))
    idirOffice_ = db.Column(db.String(2))

    def __init__(self, comName_ , serialNumber_, SID_, manufacturer_, ntVer_, operSys_, domain_, ipaddress_, netID_, MAC_, productName_, version_, GUID_, server_, inputTime_, inputDate_, ioffCode_, ioffName_, iinPak_, iinProvince_, idirOffice_ ):

        self.comName_ = comName_
        self.serialNumber_ = serialNumber_
        self.SID_ = SID_
        self.manufacturer_ = manufacturer_
        self.ntVer_ = ntVer_
        self.operSys_ = operSys_
        self.domain_ = domain_
        self.ipaddress_ = ipaddress_
        self.netID_ = netID_
        self.MAC_ = MAC_
        self.productName_ = productName_
        self.version_ = version_
        self.GUID_ = GUID_
        self.server_ = server_
        self.inputTime_ = inputTime_
        self.inputDate_ = inputDate_
        self.ioffCode_  = ioffCode_
        self.ioffName_ = ioffName_
        self.iinPak_ = iinPak_ 
        self.iinProvince_  = iinProvince_
        self.idirOffice_  = idirOffice_ 

class DataOffice(db.Model):
    __tablename__ = "office"
    id = db.Column(db.Integer, primary_key=True)
    offCode_ = db.Column(db.String(20))
    offName_ = db.Column(db.String(50))
    subNet_ = db.Column(db.String(16))
    inPak_ = db.Column(db.String(2))
    inProvince_ = db.Column(db.String(16))
    dirOffice_ = db.Column(db.String(2))

    def __init__(self, offCode_, offName_, subNet_, inPak_, inProvince_, dirOffice_):
        self.offCode_ = offCode_
        self.offName_ = offName_
        self.subNet_ = subNet_
        self.inPak_ = inPak_
        self.inProvince_ = inProvince_
        self.dirOffice_ = dirOffice_    

class UserInstall(db.Model):
    __tablename__ = "userint"

    id = db.Column(db.Integer, primary_key=True)
    username_ = db.Column(db.String(100))
    telephone_ = db.Column(db.String(15))
    email_ = db.Column(db.String(100))
    status_ = db.Column(db.String(2))

    def __int__(self, username_, telephone_, email_, status):
        self.username_ = username_
        self.telephone_ = telephone_
        self.email_ = email_
        self.status = status_
        
        
        # command >>> from api import db
    # command >>> db.create_all()






#@app.route('/')
#def hello():
#    """Renders a sample page."""
#    return "Hello World!"



@app.route('/input', methods=['POST','GET'])
def get_data():
    if request.method == 'GET':
        return "<h1>Method == GET</h1>"
    if request.method == 'POST':
        comName = request.form['ComName']
        serialNumber = request.form['SerialNumber']
        SID = request.form['SID']
        manufacturer = request.form['Manufacturer']
        ntVer = request.form['NtVer']
        operSys = request.form['OperSys']
        domain = request.form['domain']
        ipaddress = request.form['ipaddress']
        netID = request.form['NetID']
        MAC = request.form['MAC']
        productName = request.form['productname']
        version = request.form['version']
        GUID = request.form['GUID']
        server = request.form['server']
        inputTime = datetime.now().strftime("%H:%M:%S")
        inputDate = datetime.now().strftime("%Y-%m-%d")

        print(comName, serialNumber, SID, manufacturer, ntVer, operSys, domain, ipaddress, netID, MAC,
                    productName, version, GUID, server, inputTime,  inputDate)



        if db.session.query(Data).filter(Data.ipaddress_ == ipaddress).count()== 0:
            qryOffice=db.session.query(DataOffice).filter(DataOffice.subNet_==netID).first()
            ioffCode = qryOffice.offCode_  
            ioffName = qryOffice.offName_ 
            iinPak = qryOffice.inPak_ 
            iinProvince = qryOffice.inProvince_ 
            idirOffice = qryOffice.dirOffice_ 

            data=Data(comName, serialNumber, SID, manufacturer, ntVer,operSys,domain,ipaddress,netID,MAC,productName,version,GUID,server,inputTime,inputDate,ioffCode, ioffName , iinPak , iinProvince , idirOffice )
            db.session.add(data)
            db.session.commit()
            return '<H2>ระบบได้รับข้อมูลเครื่องคอมพิวเตอร์เรียบร้อย ขอบคุณครับ'
        else:
            qryIP= db.session.query(Data).filter(Data.ipaddress_==ipaddress).first()
            qryIP.comName_ = comName
            qryIP.serialNumber_ = serialNumber
            qryIP.SID_ = SID
            qryIP.manufacturer_ = manufacturer
            qryIP.ntVer_ = ntVer
            qryIP.operSys_ = operSys
            qryIP.domain_ = domain
            qryIP.netID_ = netID
            qryIP.MAC_ = MAC
            qryIP.productName_ = productName
            qryIP.version_ = version
            qryIP.GUID_ = GUID
            qryIP.server_ = server
            qryIP.inputTime_ = inputTime
            qryIP.inputDate_ = inputDate
            db.session.commit()
            return '<h2> ระบบได้ปรับปรุงข้อมูลเครื่องคอมพิวเตอร์เรียบร้อย ขแบคุณครับ'



    return 'ขอบคุณครับ'



@app.route('/')
@app.route('/home')
def home():
   
    #guests=db.session.query(Clients).join(Appointments).filter(Appointments.clientnumber==Clients.clientnumber).filter(Appointments.weekyr==weekyrnum).all()
    #guests=db.session.query(Appointments.time,Clients.name).join(Clients).filter(Appointment.clientnumber==Clients.clientnumber).filter(Appointments.weekyr==weekyrnum).all()
    #session.query(models.Model1).join(models.Model2).filter(models.Model2.name == 'TEST')
    datenow = datetime.now().strftime('%Y-%m-%d')
    yesterday=datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    resultall=db.session.query(Data).count()
    #center=db.session.query(Data).filter(Data.iinPak_=='0').count()
    dailycount = db.session.query(Data).filter(Data.inputDate_== datenow).count()
    yestcount = db.session.query(Data).filter(Data.inputDate_== yesterday).count()
    alllist  = db.session.query(Data.iinPak_, func.count(Data.iinPak_)).group_by(Data.iinPak_).all()
    center= 0 
    pak1 = 0
    pak2 = 0 
    pak3 = 0
    pak4 = 0 
    pak5 = 0
    pak6 = 0
    pak7 = 0
    pak8 = 0
    pak9 = 0
    pak10 = 0  
    pak11 = 0 
    pak12  = 0
    for x,y in alllist:
        if x == '0':
            center = y
        elif x == '1':
            pak1 = y
        elif x=='2':
            pak2 = y
        elif x == '3':
            pak3 = y
        elif x == '4':
            pak4 = y
        elif x=='5':
            pak5 = y
        elif x == '6':
            pak6 = y
        elif x == '7':
            pak7 = y
        elif x=='8':
            pak8 = y
        elif x == '9':
            pak9 = y
        elif x == '10':
            pak10 = y
        elif x=='11':
            pak11 = y
        elif x == '12':
            pak12 = y

    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        center=center,
        pak1=pak1,
        pak2=pak2,
        pak3=pak3,
        pak4=pak4, 
        pak5=pak5, 
        pak6=pak6, 
        pak7=pak7, 
        pak8=pak8, 
        pak9=pak9, 
        pak10=pak10, 
        pak11=pak11,
        pak12=pak12, 
        resultall = resultall,
        dailycount = dailycount,
        yestcount = yestcount
    
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message=''
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message=''
    )


@app.route('/install')
def install():  
    alllist  = db.session.query(Data.iinPak_, func.count(Data.iinPak_)).group_by(Data.iinPak_).all()
    resultall=db.session.query(Data).count()
    #df_alllist = pd.DataFrame(alllist)
    #alllist = db.session.query(Data.ioffName_, Data.ipaddress_, Data.inputDate_, Data.inputTime_).all()
    #label = ['Office Name','Ip Address', 'Date Install ','Time Install' ]
    #df = pd.DataFrame.from_records(alllist, columns=labels)
    #alllist = sorted(alllist, key=lambda tup: tup[0])
    center= 0 
    pak1 = 0
    pak2 = 0 
    pak3 = 0
    pak4 = 0 
    pak5 = 0
    pak6 = 0
    pak7 = 0
    pak8 = 0
    pak9 = 0
    pak10 = 0  
    pak11 = 0 
    pak12  = 0
    for x,y in alllist:
        if x == '0':
            center = y
        elif x == '1':
            pak1 = y
        elif x=='2':
            pak2 = y
        elif x == '3':
            pak3 = y
        elif x == '4':
            pak4 = y
        elif x=='5':
            pak5 = y
        elif x == '6':
            pak6 = y
        elif x == '7':
            pak7 = y
        elif x=='8':
            pak8 = y
        elif x == '9':
            pak9 = y
        elif x == '10':
            pak10 = y
        elif x=='11':
            pak11 = y
        elif x == '12':
            pak12 = y

    return render_template(
        'install.html',
        title='install',
        year=datetime.now().year,
        #alllist = alllist,
        resultall = resultall,
        center=center,
        pak1=pak1,
        pak2=pak2,
        pak3=pak3,
        pak4=pak4, 
        pak5=pak5, 
        pak6=pak6, 
        pak7=pak7, 
        pak8=pak8, 
        pak9=pak9, 
        pak10=pak10, 
        pak11=pak11,
        pak12=pak12       
        )
    




@app.route('/resultinstall')
def resultinstall():
    #offresult = db.session.query(Data.iinPak_, func.count(Data.iinPak_)).group_by(Data.iinPak_).all()
    #offresult = db.session.query(Data.ioffName_ ,Data.ioffCode_, func.count(Data.ioffName_)).group_by(Data.ioffCode_ ).all()
    offresult = db.session.query(Data.ioffName_, Data.ipaddress_, Data.inputDate_, Data.inputTime_).all() 
    df_offreuslt = pd.DataFrame(offresult)

    return render_template(
        'resultinstall.html',
        title='resultinstall',
        year=datetime.now().year,
     
        df_offreuslt = df_offreuslt
        )

@app.route('/dailyinstall')
def dailyinstall():
    #alllist = db.session.query(Data.ioffName_, Data.ipaddress_, Data.inputDate_, Data.inputTime_).all()
    #label = ['Office Name','Ip Address', 'Date Install ','Time Install' ]
    #df = pd.DataFrame.from_records(alllist, columns=labels)
    #alllist = sorted(alllist, key=lambda tup: tup[0])
    datenow = datetime.now().strftime('%Y-%m-%d')
    yesterday=datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    dailylist = db.session.query(Data.ioffName_, Data.ipaddress_, Data.inputDate_, Data.inputTime_).filter(Data.inputDate_== datenow).all()
    #alllist = db.session.query(Data.ioffName_, Data.ipaddress_, Data.inputDate_, Data.inputTime_).all()
    #label = ['Office Name','Ip Address', 'Date Install ','Time Install' ]
    #df = pd.DataFrame.from_records(alllist, columns=labels)
    #alllist = sorted(alllist, key=lambda tup: tup[0])
    alllist  = db.session.query(Data.iinPak_, func.count(Data.iinPak_)).filter(Data.inputDate_== datenow).group_by(Data.iinPak_).all()
    resultall=db.session.query(Data).count()
    
    center= 0 
    pak1 = 0
    pak2 = 0 
    pak3 = 0
    pak4 = 0 
    pak5 = 0
    pak6 = 0
    pak7 = 0
    pak8 = 0
    pak9 = 0
    pak10 = 0  
    pak11 = 0 
    pak12  = 0
    for x,y in alllist:
        if x == '0':
            center = y
        elif x == '1':
            pak1 = y
        elif x=='2':
            pak2 = y
        elif x == '3':
            pak3 = y
        elif x == '4':
            pak4 = y
        elif x=='5':
            pak5 = y
        elif x == '6':
            pak6 = y
        elif x == '7':
            pak7 = y
        elif x=='8':
            pak8 = y
        elif x == '9':
            pak9 = y
        elif x == '10':
            pak10 = y
        elif x=='11':
            pak11 = y
        elif x == '12':
            pak12 = y
    return render_template(
        'dailyinstall.html',
        title='dailyinstall',
        year=datetime.now().year,
        dailylist=dailylist,
        center=center,
        pak1=pak1,
        pak2=pak2,
        pak3=pak3,
        pak4=pak4, 
        pak5=pak5, 
        pak6=pak6, 
        pak7=pak7, 
        pak8=pak8, 
        pak9=pak9, 
        pak10=pak10, 
        pak11=pak11,
        pak12=pak12  

        )



if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
