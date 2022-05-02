from concurrent.futures import thread
from sqlite3 import threadsafety
import cv2
from flask import Flask, request , render_template
from config import GMAIL_ID, GMAIL_PASSWORD
import platform_utility as pf
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import os
import threading
from datetime import date
from util import *


classes = {'pins_Adriana Lima': 0, 'pins_Alex Lawther': 1, 'pins_Alexandra Daddario': 2, 'pins_Alvaro Morte': 3, 'pins_Amanda Crew': 4, 'pins_Andy Samberg': 5, 'pins_Anne Hathaway': 6, 'pins_Anthony Mackie': 7, 'pins_Avril Lavigne': 8, 'pins_Ben Affleck': 9, 'pins_Bill Gates': 10, 'pins_Bobby Morley': 11, 'pins_Brenton Thwaites': 12, 'pins_Brian J. Smith': 13, 'pins_Brie Larson': 14, 'pins_Chris Evans': 15, 'pins_Chris Hemsworth': 16, 'pins_Chris Pratt': 17, 'pins_Christian Bale': 18, 'pins_Cristiano Ronaldo': 19, 'pins_Danielle Panabaker': 20, 'pins_Dominic Purcell': 21, 'pins_Dwayne Johnson': 22, 'pins_Eliza Taylor': 23, 'pins_Elizabeth Lail': 24, 'pins_Emilia Clarke': 25, 'pins_Emma Stone': 26, 'pins_Emma Watson': 27, 'pins_Gwyneth Paltrow': 28, 'pins_Henry Cavil': 29, 'pins_Hugh Jackman': 30, 'pins_Inbar Lavi': 31, 'pins_Irina Shayk': 32, 'pins_Jake Mcdorman': 33, 'pins_Jason Momoa': 34, 'pins_Jennifer Lawrence': 35, 'pins_Jeremy Renner': 36, 'pins_Jessica Barden': 37, 'pins_Jimmy Fallon': 38, 'pins_Johnny Depp': 39, 'pins_Josh Radnor': 40, 'pins_Katharine Mcphee': 41, 'pins_Katherine Langford': 42, 'pins_Keanu Reeves': 43, 'pins_Krysten Ritter': 44, 'pins_Leonardo DiCaprio': 45, 'pins_Lili Reinhart': 46, 'pins_Lindsey Morgan': 47, 'pins_Lionel Messi': 48, 'pins_Logan Lerman': 49, 'pins_Madelaine Petsch': 50, 'pins_Maisie Williams': 51, 'pins_Maria Pedraza': 52,
           'pins_Marie Avgeropoulos': 53, 'pins_Mark Ruffalo': 54, 'pins_Mark Zuckerberg': 55, 'pins_Megan Fox': 56, 'pins_Miley Cyrus': 57, 'pins_Millie Bobby Brown': 58, 'pins_Morena Baccarin': 59, 'pins_Morgan Freeman': 60, 'pins_Nadia Hilker': 61, 'pins_Natalie Dormer': 62, 'pins_Natalie Portman': 63, 'pins_Neil Patrick Harris': 64, 'pins_Pedro Alonso': 65, 'pins_Penn Badgley': 66, 'pins_Rami Malek': 67, 'pins_Rebecca Ferguson': 68, 'pins_Richard Harmon': 69, 'pins_Rihanna': 70, 'pins_Robert De Niro': 71, 'pins_Robert Downey Jr': 72, 'pins_Sarah Wayne Callies': 73, 'pins_Selena Gomez': 74, 'pins_Shakira Isabel Mebarak': 75, 'pins_Sophie Turner': 76, 'pins_Stephen Amell': 77, 'pins_Taylor Swift': 78, 'pins_Tom Cruise': 79, 'pins_Tom Hardy': 80, 'pins_Tom Hiddleston': 81, 'pins_Tom Holland': 82, 'pins_Tuppence Middleton': 83, 'pins_Ursula Corbero': 84, 'pins_Wentworth Miller': 85, 'pins_Zac Efron': 86, 'pins_Zendaya': 87, 'pins_Zoe Saldana': 88, 'pins_alycia dabnem carey': 89, 'pins_amber heard': 90, 'pins_barack obama': 91, 'pins_barbara palvin': 92, 'pins_camila mendes': 93, 'pins_elizabeth olsen': 94, 'pins_ellen page': 95, 'pins_elon musk': 96, 'pins_gal gadot': 97, 'pins_grant gustin': 98, 'pins_jeff bezos': 99, 'pins_kiernen shipka': 100, 'pins_margot robbie': 101, 'pins_melissa fumero': 102, 'pins_scarlett johansson': 103, 'pins_tom ellis': 104}


class_names = list(classes.keys())
TEMP = 0.0
MOTION=0
app = Flask(__name__)
dir = os.getcwd()
db = SQLAlchemy(app)
file_path = os.path.abspath(os.getcwd())+"\class.db"
app.config['SESSION_SQLALCHEMY'] = db
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////" + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = GMAIL_ID,
    MAIL_PASSWORD = GMAIL_PASSWORD
)

class Students(db.Model):
    """This class defines model used for Student table in Database."""

    stud_name = db.Column(db.String(80), primary_key=True)
    attendance = db.Column(db.Integer, nullable=False,default=0)
    attentive = db.Column(db.Integer, nullable=False,default=-1)

    def __init__(self, stud_name, attendance, attentive):
        self.stud_name = stud_name
        self.attendance = attendance
        self.attentive = attentive

class Teacher(db.Model):
    """This class defines model used for Teacher table in Database."""

    teacher_name = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, teacher_name, email, password ):
        self.teacher_name = teacher_name
        self.email = email
        self.password = password
    

def extract_faces(collage):
    res = []
    gray1 = cv2.cvtColor(collage, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
    faces = faceCascade.detectMultiScale(
        gray1,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(collage, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_color = collage[y:y + h, x:x + w]
        resized = cv2.resize(roi_color, (160, 160), interpolation=cv2.INTER_AREA)
        # print("resize type : ", type(resized))
        temp_image  = resized.tolist()
        res.append(temp_image)
    return res



def get_updates_async(i):
    collage = pf.getsensordata1(str(i))
    collage = collage['image']
    # print("COllage type: ", type(collage))
    A = np.array(collage,dtype=np.uint8)
    im = Image.fromarray(A)
    img_name = 'cam' + str(i) + '.jpg'
    # im.show()
    file_path = os.path.abspath(os.getcwd()) + "/static/" + img_name
    im.save(file_path)
    # im.show()
    images = extract_faces(collage=A)
    for image in images:
        data = {
            'image':image
        }
        student_name = pf.getmodeldata('1',data,'/model/1')
        student_name = student_name.lower()
        print("Student_name: ",student_name)
        emotion_status = int(pf.getmodeldata('2',data,'/model/1'))
        
        stud = Students.query.filter_by(stud_name=student_name).first()
        print("Stud: ", stud)
        # stud = Students.query.get(student_name)
        stud.attendance = 1
        stud.attentive = emotion_status
        db.session.commit()

@app.route('/get_updates', methods=['POST','GET'])
def get_updates():
    positive_emotions = 0
    negative_emotions = 0
    student_dict = dict()
    t_list = [None]*3
    for i in range(1,4):
        t_list[i-1] = threading.Thread(target=get_updates_async, args=(i,))
        t_list[i-1].start()
    #    return {"key":"cool"}
    for i in range(3):
        t_list[i].join()
    student_list = Students.query.all()
    total_present_students = 0
    for student in student_list:
        if student.attentive == 1:
            positive_emotions = positive_emotions + 1
            total_present_students += 1
            student_dict[student.stud_name] = 1

        elif student.attentive == 0:
            negative_emotions = negative_emotions + 1
            total_present_students += 1
            student_dict[student.stud_name] = 1
            
        else:
            student_dict[student.stud_name] = 0
    if(total_present_students==0):
        total_present_students =1
    attentive =  (positive_emotions * 100)/total_present_students
    res = {
        'attend':student_dict,
        'attentive': attentive
    }
    print("Data Sent to Client")
    return res,200 

@app.route('/start_class', methods=['POST'])
def start_class():
    students = Students.query.all()
    for student in students:
        student.attendance = 0
    db.session.commit()
    return "Class Started"

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    teacher_name = request.form['username']
    password = request.form['password']
    check_user = Teacher.query.filter_by(teacher_name=teacher_name).first()
    if(check_user is not None):
        if(check_user.password == password):
            return render_template('home.html',user=teacher_name)
        else:
            return render_template('login.html',err_msg= "Incorrect Password!!")
    else:
        return render_template('login.html',err_msg= "No such User exists!!")

@app.route('/signup', methods=['GET','POST'])
def signup():
   #Function to process User SignUp request
    if request.method == "GET":
        return render_template('signup.html')
    teacher_name = request.form['username']
    password = request.form['password']
    email = request.form['email']
    check_user = Teacher.query.filter_by(teacher_name=teacher_name).first()
    if(check_user is not None):
        return render_template('signup.html',err_msg= "User already registered, please LogIn!!")
    else:
        user = Teacher(teacher_name=teacher_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        return render_template('signup.html',succ_msg= "Registered Successfully!!")


@app.route('/', methods=['GET','POST'])
@app.route('/logout', methods=['GET','POST'])
def index():
     return render_template('signup.html')

@app.route('/detect_motion', methods=['GET'])
def motiond():
    data = dict()
    t = 0
    m = MOTION
    print("Motion to send: ",m)
    print("Temp to send: ", TEMP)
    if(m==1):
        if(TEMP<25):
            t = 0
        elif TEMP>=25 and TEMP<27:
            t = 1
        elif TEMP>=27 and TEMP<29:
            t = 2
        elif TEMP>=29 and TEMP<32:
            t = 3
        else:
            t = 4
        data={
            'motion':1,
            'fan':t
        }


    else:
        data={
            'motion':0,
            'fan':t
        }
    
    pf.setcontrollerdata('6',t)
    pf.setcontrollerdata('7',m)

    return data

def motiondetector():
    global MOTION
    motionsensorid = '4'
    motionmodelid = '3'
    prevframe = None
    while(1):
        frame = []
        if prevframe != None:
            frame.append(prevframe)

        for x in range(2):
            frame.append(pf.getsensordata1(motionsensorid)['image'])
            print("frame num: ",x)
            print("Shape: ", np.array(frame[x]).shape)
        data = {
            'image':frame
        }
        MOTION = int(pf.getmodeldata(motionmodelid,data,'/model/1'))
        print("Motion: ", MOTION)

def tempdata():
    global TEMP
    tempsensorid = '5'
    while(1):
        TEMP = pf.getsensordata1(tempsensorid)
        print("Temp: ", TEMP)
    


@app.route('/end_class', methods=['POST','GET'])
def end_class():
    username = request.get_json()['username'] # "username":"<username>"
    user = Teacher.query.filter_by(teacher_name=username).first()
    user_email = user.email

    students = Students.query.all()
    title = """Hello """+username+"""
This is attendance for your class"""
    body = """DATE: """
    today = date.today()
    dt = today.strftime("%d/%m/%Y")
    body = body + str(dt) + "\n"
    for student in students:
        name = student.stud_name
        attendance = student.attendance
        body = body + name + " : "+attendance + "\n"
    try:
        email_service(user_email=user_email,
                email_title=title, 
                body=body)
    except Exception as e:
        print(e)
        return "fail"
    return "pass"


if __name__ == "__main__":
    db.create_all()
    db.session.commit()
    for i in class_names:
        try:
            i = i[5:].lower()
            student = Students(stud_name=i,attendance=0,attentive=-1)
            db.session.add(student)
            db.session.commit()
        except Exception as e:
            print(e)
            break
    # t_list = [None]*3
    # for i in range(1,4):
    #     t_list[i-1] = threading.Thread(target=pf.getsensordata1, args=(str(i),))
    #     t_list[i-1].start()
    #    return {"key":"cool"}

    t1 = threading.Thread(target = motiondetector)
    t1.start()
    t2 = threading.Thread(target = tempdata)
    t2.start()

    app.run(debug=False, port=5000, host='0.0.0.0',threaded=True)