from flask import Flask, render_template, request
import mysql.connector
from apiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from datetime import datetime, timedelta


Combined_calendar_data=[]
scopes = ['https://www.googleapis.com/auth/calendar.readonly','https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/calendar.events']
flow =  InstalledAppFlow.from_client_secrets_file("client_secret.json",scopes=scopes)
#credentials = flow.run_console()
#pickle.dump(credentials, open("token.pkl","wb"))

credentials = pickle.load(open("token.pkl","rb"))
service = discovery.build("calendar","v3",credentials= credentials)

result = service.calendarList().list().execute()

ComingEvents = []
EndedEvents = []

calendar_id = result['items'][0]['id']
start_date = datetime.now().isoformat() +'Z'
events = service.events().list(calendarId=calendar_id, timeMin=start_date,).execute()

eventsEnded = service.events().list(calendarId=calendar_id, timeMax=start_date,).execute()
for i in eventsEnded['items']:
    if(i['summary']=='Medical Appointment'):
        d =i['start']['dateTime']
        d = d[:-9]
        dt = datetime.strptime(d, '%Y-%m-%dT%H:%M')
        dt = dt.strftime('Date %Y-%m-%d Time %H:%M')  
        t =i['end']['dateTime']
        t = t[:-9]
        tt = datetime.strptime(t, '%Y-%m-%dT%H:%M')
        tt = tt.strftime('Date %Y-%m-%d Time %H:%M')
        EndedEvents.append((i['summary'],i['description'],dt,tt))

for event in events['items']:
    if(event['summary']=='Medical Appointment'):
        d =event['start']['dateTime']
        d = d[:-9]
        dt = datetime.strptime(d, '%Y-%m-%dT%H:%M')
        dt = dt.strftime('Date %Y-%m-%d Time %H:%M')  
        t =event['end']['dateTime']
        t = t[:-9]
        tt = datetime.strptime(t, '%Y-%m-%dT%H:%M')
        tt = tt.strftime('Date %Y-%m-%d Time %H:%M')
        ComingEvents.append((event['summary'],event['description'],dt,tt))

app = Flask(__name__)


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="NewPassword",
  database="gynecology"
)
mycursor = mydb.cursor()

@app.route('/home')
def home():
   return render_template('index.html')

@app.route('/index_admin')
def index_admin():
   return render_template('index_admin.html')

@app.route('/index_doctor')
def index_doctor():
   return render_template('index_doctor.html')


@app.route('/contact', methods=['POST', 'GET'])
def contact():
   if request.method == 'POST':  ##check if there is post data
      name = request.form['name']
      email = request.form['email']
      message = request.form['message']
      sql = "INSERT INTO complaint (email,name,complainttext) VALUES (%s,%s,%s)"
      val= (email,name,message)
      mycursor.execute(sql, val)
      mydb.commit()
      return render_template('index.html')
   else:
      return render_template('contact.html')

@app.route('/', methods=['POST', 'GET'])
def login():
   if request.method == 'POST':  ##check if there is post data
      id = request.form['id']
      Role = request.form['Role']
      password = request.form['password']
      u= int(id)
      idd=-1
      if(Role == '3'):
         sql1 = mycursor.execute("SELECT D_ID From doctor")
         ID = mycursor.fetchall()
         sql2 = mycursor.execute("SELECT password From doctor")
         PASSWORD = mycursor.fetchall()
         for i in ID:
            for inneri in i:
               idd = idd+1
               if(inneri==u):
                        if(password == PASSWORD[idd][0]):
                           return render_template('index_doctor.html')
                        else:
                           return render_template('login.html')
               else: render_template('login.html') 
         return render_template('login.html')
      elif(Role == '1'):
         sql1 = mycursor.execute("SELECT P_ID From patient")
         ID = mycursor.fetchall()
         sql2 = mycursor.execute("SELECT password From patient")
         PASSWORD = mycursor.fetchall()
         for i in ID:
            for inneri in i:
               idd = idd+1
               if(inneri==u):
                        if(password == PASSWORD[idd][0]):
                           return render_template('index.html')
                        else:
                           return render_template('login.html')
               else: render_template('login.html') 
         return render_template('login.html')
      elif(Role == '2'):
         sql1 = mycursor.execute("SELECT A_ID From admin")
         ID = mycursor.fetchall()
         sql2 = mycursor.execute("SELECT password From admin")
         PASSWORD = mycursor.fetchall()
         for i in ID:
            for inneri in i:
               idd = idd+1
               if(inneri==u):
                        if(password == PASSWORD[idd][0]):
                           return render_template('index_admin.html')
                        else:
                           return render_template('login.html')
               else: render_template('login.html') 
         return render_template('login.html')
      else:
         return render_template('login.html')
   else:
      return render_template('login.html')


@app.route('/bookAppointment', methods=['POST', 'GET'])
def bookAppointment():
   if request.method == 'POST':  ##check if there is post data
        StartDate = request.form['Appointmenttime']
        StartDate1 = StartDate + ':00+02:00'
        dt = datetime.strptime(StartDate, '%Y-%m-%dT%H:%M')
        EndDate1 = dt + timedelta(hours = 4)
        EndDate2 = EndDate1.strftime('%Y-%m-%dT%H:%M') +':00+02:00'
        Desciption = request.form['description']
        DID = request.form['DID']
        PID = request.form['PID']
        RNum = request.form['RNum']
        Urgency = request.form['Urgency']
        sql = "INSERT INTO appointment (Patient_P_ID,date,DOCTOR_D_ID,ROOM_Room_number,Urgency,symptoms) VALUES (%s,%s,%s,%s,%s,%s)"
        val= (PID,StartDate1,DID,RNum,Urgency,Desciption)
        mycursor.execute(sql, val)
        mydb.commit()
        event = {
                'summary': 'Medical Appointment',
                'location': 'Online',
                'description': Desciption,
                'start': {
                    'dateTime': StartDate1,
                    'timeZone': 'Africa/Cairo',
                },
                'end': {
                    'dateTime': EndDate2,
                    'timeZone': 'Africa/Cairo',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                    ],
                },
                }
        insert = service.events().insert(calendarId=calendar_id, body=event).execute()
        return render_template('index.html')
   else:
        return render_template('bookAppointment.html')

    


   


@app.route('/signup',methods = ['POST', 'GET'])
def signup():
    if request.method == "POST":
        role = request.form['role']
        if role == "Doctor":
            return render_template("signupDoctor.html")
            return render_template("signupPatient.html")

    return render_template("signup.html")    





@app.route('/signupDoctor',methods = ['POST', 'GET'])
def signupDoctor():
   if request.method == 'POST':
      fname = request.form['first_name']
      lname = request.form['last_name']
      email = request.form['email']
      phone = request.form['phone_number']
      aptnum = request.form['aptNumber']
      stname = request.form['StName']
      password = request.form['Password']
      gender = request.form['Gender']
      did = request.form['DID']
      ssn = request.form['DSSN']
      sal = request.form['Salary']

      sql = "insert into doctor (fname, lname, D_ID, D_SSN, apt_number, st_name, salary, gender, email, password, phone_number) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
      val = (fname, lname, did, ssn, aptnum, stname, sal, gender, email, password, phone)

      mycursor.execute(sql, val)
      mydb.commit()
      return render_template('index_doctor.html')
   else:
      return render_template('signupDoctor.html')
@app.route('/signupPatient', methods = ['POST', 'GET'])
def signupPatient():
   if request.method == 'POST':
      fname = request.form['first_name']
      lname = request.form['last_name']
      email = request.form['email']
      phone = request.form['phone_number']
      password = request.form['Password']
      Pid = request.form['pid']
      aptnum = request.form['AptNumber']
      stname = request.form['StName']

      sql = "insert into patient (P_ID, fname, lname, email, password, phone_number, apt_number, st_name) values (%s, %s, %s, %s, %s, %s, %s, %s)"
      val = (Pid, fname, lname, email, password, phone, aptnum, stname)

      mycursor.execute(sql, val)
      mydb.commit()
      return render_template('index.html')
   else:
      return render_template('signupPatient.html')

@app.route('/addentry')
def addentry():
    


   return render_template('Add Entry.html')

@app.route('/admin')
def Admin():
    


   return render_template('Admin.html')    

@app.route('/viewAppointment')
def viewAppointment():
    mycursor.execute("SELECT * From appointment")
    view_headers = [x[0] for x in mycursor.description]
    viewData = mycursor.fetchall()
    
    sql = "SELECT * From appointment WHERE Patient_P_ID = %s"
    val= [8]
    mycursor.execute(sql, val)
    d= mycursor.fetchall()

    data = {
        'rec' : d,
        'header' : view_headers
    }
    
    
    return render_template('viewAppointment.html', data = data)

@app.route('/viewNurses')
def viewNurses():
    mycursor.execute("SELECT * From nurse")
    view_headers = [x[0] for x in mycursor.description]
    viewData = mycursor.fetchall()
    data = {
        'rec' : viewData,
        'header' : view_headers
    }
    
    
    return render_template('viewPatients.html', data = data)

@app.route('/viewPatients')
def viewPatients():
    mycursor.execute("SELECT * From patient")
    view_headers = [x[0] for x in mycursor.description]
    viewData = mycursor.fetchall()
    data = {
        'rec' : viewData,
        'header' : view_headers
    }
    
    
    return render_template('viewPatients.html', data = data)

@app.route('/viewDoctors')
def viewDoctors():
    mycursor.execute("SELECT * From doctor")
    view_headers = [x[0] for x in mycursor.description]
    viewData = mycursor.fetchall()
    data = {
        'rec' : viewData,
        'header' : view_headers
    }
    
    
    return render_template('viewDoctors.html', data = data)


@app.route('/viewRoom')
def viewRoom():
    mycursor.execute("SELECT * From room")
    view_headers = [x[0] for x in mycursor.description]
    viewData = mycursor.fetchall()
    data = {
        'rec' : viewData,
        'header' : view_headers
    }
    
    
    return render_template('viewRoom.html', data = data)

@app.route('/viewData')
def viewData():
    #to view rooms or patients or doctors or appointment


   return render_template('viewData.html')

@app.route('/viewAppointmentDoctor', methods=['POST', 'GET'])
def ViewPatientDoctor():
    #mycursor.execute("SELECT * From conact")
    #view_headers = [x[0] for x in mycursor.description]
    #viewData = mycursor.fetchall()
    
    return render_template('viewAppointmentDoctor.html', data = ComingEvents)

@app.route('/viewAppointmentHistoryDoctor', methods=['POST', 'GET'])
def ViewAppointmentHistoryDoctor():
    #mycursor.execute("SELECT * From conact")
    #view_headers = [x[0] for x in mycursor.description]
    #viewData = mycursor.fetchall()
    
    return render_template('viewAppointmentHistoryDoctor.html', data = EndedEvents)



if __name__ == '__main__':
   app.run()