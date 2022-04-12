from flask import Flask, render_template, request, session
from datetime import datetime, timedelta

import time
from flask_sqlalchemy import SQLAlchemy
import json

from sqlalchemy import desc
from werkzeug.utils import secure_filename, redirect
import os
import random
from flask_mail import Mail
app = Flask(__name__)

with open('config.json') as c:
    params = json.load(c)["params"]
app.secret_key = "super-secret-key"
app.config['cv_path'] = params['cv_path']
app.config['dp_path'] = params['dp_path']
app.config['image_path'] = params['image_path']
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT="465",
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['email'],
    MAIL_PASSWORD=params['password']
)
mail = Mail(app)

db = SQLAlchemy(app)

class Enquiry(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    cno = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    gen = db.Column(db.String(6), unique=False, nullable=False)
    city = db.Column(db.String(30), unique=False, nullable=False)
    enquiry = db.Column(db.String(100), unique=False, nullable=False)
    date = db.Column(db.String(20), unique=False, nullable=True, default=datetime.now())
    status = db.Column(db.String(1), unique=False, nullable=False, default='N')

class Feedback(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    email_id = db.Column(db.String(40), unique=False, nullable=False)
    contact_no= db.Column(db.String(40), unique=False, nullable=False)
    feedback = db.Column(db.String(40), unique=False, nullable=False)
    date = db.Column(db.String(40), unique=False, nullable=True, default=datetime.now())
    status = db.Column(db.String(40), unique=False, nullable=False, default='N')

class Career(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    contact = db.Column(db.String(40), unique=False, nullable=False)
    gender = db.Column(db.String(8), unique=False, nullable=False)
    address = db.Column(db.String(40), unique=False, nullable=False)
    cv = db.Column(db.String(40), unique=False, nullable=False)
    city = db.Column(db.String(8), unique=False, nullable=False)
    date = db.Column(db.String(40), unique=False, nullable=True, default=datetime.now())
    status = db.Column(db.String(40), unique=False, nullable=False, default='N')

class Register(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    contact = db.Column(db.String(40), unique=False, nullable=False)
    address = db.Column(db.String(100), unique=False, nullable=False)
    city= db.Column(db.String(40), unique=False, nullable=False)
    status = db.Column(db.String(40), unique=False, nullable=False)
    gender = db.Column(db.String(40), unique=False, nullable=False)
    dd = db.Column(db.String(40), unique=False, nullable=False)
    duration = db.Column(db.String(40), unique=False, nullable=False)
    bank = db.Column(db.String(40), unique=False, nullable=False)
    date = db.Column(db.String(20), unique=False, nullable=True, default=datetime.now())

class Login(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    password = db.Column(db.String(40), unique=False, nullable=False)
    status = db.Column(db.String(8), unique=False, nullable=False, default='C')

class Member(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    contact = db.Column(db.String(40), unique=False, nullable=False)
    address = db.Column(db.String(100), unique=False, nullable=False)
    city= db.Column(db.String(40), unique=False, nullable=False)
    status = db.Column(db.String(40), unique=False, nullable=False)
    gender = db.Column(db.String(40), unique=False, nullable=False)
    date = db.Column(db.String(20), unique=False, nullable=True, default=datetime.now())

class Services(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(40), unique=False, nullable=False)
    detail = db.Column(db.String(300), unique=False, nullable=False)
    image = db.Column(db.String(40), unique=False, nullable=False)

class Requests(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=False, nullable=False)
    email = db.Column(db.String(300), unique=False, nullable=False)
    service = db.Column(db.String(40), unique=False, nullable=False)
    date = db.Column(db.String(40), unique=False, nullable=False)
    slot = db.Column(db.String(40), unique=False, nullable=False)
    detail = db.Column(db.String(40), unique=False, nullable=False)
    status = db.Column(db.String(8), unique=False, nullable=False, default='0')

class Reply(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    username = db.Column(db.String(40), unique=False, nullable=False)
    reply = db.Column(db.String(300), unique=False, nullable=False)
    date = db.Column(db.String(40), unique=False, nullable=True, default=datetime.now())
    time = db.Column(db.String(40), unique=False, nullable=False,default=datetime.now())

class Member_service(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    mid = db.Column(db.String(40), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    dd = db.Column(db.String(40), unique=False, nullable=False)
    plan = db.Column(db.String(40), unique=False, nullable=False)
    bank = db.Column(db.String(40), unique=False, nullable=False)
    date = db.Column(db.String(20), unique=False, nullable=True, default=datetime.now())


def get_password(n):
    s = "qwertyupkjhgfdsazxcvbnmQWERTYUPLKJHGFDSAZXCVBNM23456789"
    str = ''
    for i in range(0, n):
        a = random.randint(0, len(s))
        str += s[a]
    return str

@app.route('/')
def index():
    pid=0
    return render_template('index.html',pid=pid)

@app.route('/about')
def about():
    pid=1
    return render_template('about.html',pid=pid)


@app.route('/services')
def services():
    pid=5
    data=Services.query.all()
    return render_template('services.html',pid=pid,data=data)

@app.route('/enquiry', methods=['GET', 'POST'])
def enquiry():
    msg = ''
    pid = 2
    if request.method == 'POST':
        name = request.form.get('name')
        contact = request.form.get('cno')
        email = request.form.get('email')
        gender = request.form.get('gen')
        city = request.form.get('city')
        enq = request.form.get('enq')

        sql = Enquiry(name=name, cno=contact, gen=gender, city=city, enquiry=enq, email=email)
        db.session.add(sql)
        db.session.commit()
        msg = 'Enquiry saved successfully'

    return render_template('enquiry.html', pid=pid)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    msg = ''
    pid = 3
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('cno')
        feed = request.form.get('feed')

        sql = Feedback(name=name, email_id=email, contact_no=contact, feedback=feed)
        db.session.add(sql)
        db.session.commit()
        msg = 'Feedback saved successfully'
    return render_template('contact.html', pid=pid,msg=msg)

@app.route('/career', methods=['GET', 'POST'])
def career():
    name = ""
    email = ""
    cno = ""
    gen = ""
    msg = ""
    add=""
    city=""
    pid = 4
    if request.method == 'POST':
        msg = "Your career details saved"
        name = request.form.get('name')
        cno = request.form.get('cno')
        gender = request.form.get('gen')
        email = request.form.get('email')
        add = request.form.get('add')
        city = request.form.get('city')
        file = request.files['cv']
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]
        if ext == ".pdf" or ext == ".doc" or ext == ".docx":
            data = Career.query.filter_by(email=email).first()
            if not data:
                data = Career.query.order_by(Career.sno.desc()).first()
                if not data:
                    fname = secure_filename("1" + ext)
                else:
                    fname = secure_filename(str(int(data.sno) + 1) + ext)
                entry = Career(name=name, email=email, contact=cno, gender=gender, address=add, city=city,
                               cv=fname)
                db.session.add(entry)
                db.session.commit()
                print(fname)
                file.save(os.path.join(app.config['cv_path'], fname))
                name = ""
                email = ""
                cno = ""
                gen = ""
                city=""
                add="" 
                msg = "Career Detail Successfully Saved"
            else:
                msg = 'Email-Id already exist'
        else:
            msg = "Please upload a valid CV File"

    li1 = [name, email, cno, gen,add,city, msg]
    return render_template('career.html', li=li1, pid=pid)

@app.route('/register', methods=['GET', 'POST'])
def register():

    name = ""
    email = ""
    cno = ""
    gen = ""
    msg = ""
    city = ""
    status = ""
    add = ""
    plan = ""
    dd = ""
    bank = ""
    pid = 5

    if request.method == 'POST':

        name = request.form.get('name')
        cno = request.form.get('cno')
        gen = request.form.get('gender')
        email = request.form.get('email')
        city = request.form.get('city')
        add = request.form.get('add')
        status = request.form.get('status')
        dd= request.form.get('dd')
        bank= request.form.get('bank')
        plan=request.form.get('plan')
        data = Register.query.filter_by(email=email).first()
        if not data:

            entry = Register(name=name,email=email, contact=cno, gender=gen,city=city,address=add,status=status,dd=dd,bank=bank,duration=plan)
            db.session.add(entry)
            db.session.commit()
            mail.send_message('Message from ' + "eLearning",
                                  sender=params['email'],
                                  recipients=[email],
                                  body="Hello " + name + "\nYour details are received. We contact you soon ")
            msg = "Your details saved"


        else:
            msg="Email id already exist"
    return render_template('register.html',msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    email = ""
    password= ""

    if request.method=='POST':

        email = request.form.get('email')
        password = request.form.get('pass')

        data = Login.query.filter_by(email=email).first()
        if not data:
            msg = "Email does not exist"

        else:
            if data.password == password:
                session['name'] = data.username
                session['uid'] = data.email
                session['id'] = data.sno
                status = data.status
                data = Member_service.query.filter_by(mid=session['id']).order_by(desc(Member_service.sno)).first()
                if data:
                    date1 = data.date
                    print("date",date1)
                    duration = data.plan
                    if duration == '6 months':
                        day = 180
                    elif duration == '12 months':
                        day = 365
                    elif duration == '18 months':
                        day = 540
                    elif duration == '24 months':
                        day = 730
                    date1 = date1[:10]

                    from datetime import date
                    y = int(date1[0:4])
                    m = int(date1[5:7])
                    d = int(date1[8:10])
                    a = date(y, m, d) + timedelta(days=day)
                    print(a)
                    today = datetime.now()
                    today = datetime.strftime(today, "%Y-%m-%d")
                    y1 = int(today[0:4])
                    m1 = int(today[5:7])
                    d1 = int(today[8:10])
                    b = date(y1, m1, d1)
                    rem = a - b
                    rem = str(rem)
                    final = ""
                    final = rem.split()[0]
                    final = int(final)
                    if final <= 0:
                        final = 0
                    session['final']=final
                    print(session['final'])
                if status == 'A':
                    return render_template('user/admin/index.html')
                else:
                    return render_template('user/client/index.html')

            else:
                msg = "Invalid password"
    return render_template('login.html')

@app.route('/application/<string:sno>', methods=['GET', 'POST'])
def application(sno):
        name = ''
        email = ''
        contact = ''
        gender = ''
        city = ' '  
        date = ''
        bank = ''
        ddno = ''
        status = ''
        add = ''
        duration = ' '

        if request.method == 'POST' and 'Confirm' in request.form:

            data = Login.query.order_by(Login.sno.desc()).first()
            if not data:
                sn = 1
            else:
                sn = int(data.sno) + 1
            upass = get_password(6)
            data = Register.query.filter_by(sno=sno).first()
            entry = Login(sno=sn, username=data.name, email=data.email, password=upass, status=data.status)
            db.session.add(entry)
            db.session.commit()
            mail.send_message('Message from ' + "eLearning",
                              sender=params['email'],
                              recipients=[data.email],
                              body="Hello " + data.name + "\nYour details are verified.You can use our services "+"Your password is :"+upass)

            data = Member.query.filter_by(email=email).first()
            if not data:
                data = Register.query.filter_by(sno=sno).first()
                email = data.email
                entry = Member(sno=sn,name=data.name,email=data.email, contact=data.contact, gender=data.gender,city=data.city,address=data.address,status=data.status)
                db.session.add(entry)
                db.session.commit()

                entry = Member_service(mid=sn,email=data.email,bank=data.bank,dd=data.dd,plan=data.duration)
                db.session.add(entry)
                db.session.commit()

                data=Register.query.filter_by(sno=sno).first()
                db.session.delete(data)
                db.session.commit()
                sno = '0'

        elif request.method == 'POST' and 'Delete' in request.form:
            data = Register.query.filter_by(sno=sno).first()
            db.session.delete(data)
            db.session.commit()
            sno = '0'

        if sno != '0':
            data = Register.query.filter_by(sno=sno).first()
            sno = data.sno
            name = data.name
            email = data.email
            contact = data.contact
            gender = data.gender
            duration = data.duration
            date = data.date
            bank = data.bank
            ddno = data.dd
            add=data.address
        data = Register.query.all()
        li = [sno, name, email, contact, gender, duration, date, bank, ddno,add]
        return render_template('user/admin/application.html', data=data,li=li)


@app.route('/member/<string:cmd>,<string:sno>', methods=['GET', 'POST'])
def member(cmd,sno):
    name = ''
    email = ''
    contact = ''
    gender = ''
    city = ' '
    date = ''
    bank = ''
    ddno = ''
    status = ''
    add = ''
    duration = ' '

    if request.method == 'POST' and 'Delete' in request.form:
        data = Member.query.filter_by(sno=sno).first()
        db.session.delete(data)
        db.session.commit()
        sno='0'
        cmd='2'

    if sno!='0':
        data = Member.query.filter_by(sno=sno).first()
        sno = data.sno
        name = data.name
        email = data.email
        contact = data.contact
        gender = data.gender
        duration = data.duration
        add = data.address

    elif cmd=='1':
        data = Member.query.filter_by(status='Clients').all()
    elif cmd=='2':
        data = Member.query.filter_by(status='Worker').all()
    li=[cmd,sno,name,email,contact,gender,duration,add]


    return render_template('user/admin/member.html', data=data,li=li)

@app.route('/add_services', methods=['GET', 'POST'])
def add_services():
    pid=7
    name = ''
    detail = ''
    fname= ' '
    if request.method == 'POST':
        name = request.form.get('name')
        detail = request.form.get('detail')
        file = request.files['img']
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]
        if ext == ".jpg" or ext == ".png" or ext == ".pdf" or ext == ".jpeg":
                data = Services.query.order_by(Services.sno.desc()).first()
                if not data:
                    fname = secure_filename("1" + ext)
                else:
                    fname = secure_filename(str(int(data.sno) + 1) + ext)
                entry = Services(service=name, detail=detail, image=fname)
                db.session.add(entry)
                db.session.commit()

                file.save(os.path.join(app.config['image_path'], fname))
        else:
            msg="Invalid image"
    return render_template('user/admin/services.html')

@app.route('/admin_services/<string:sno>', methods=['GET', 'POST'])
def admin_services(sno):
    name = ''
    detail = ''

    if request.method == 'POST' and 'Modify' in request.form:
        name = request.form.get('name')
        detail = request.form.get('detail')
        sno=session['sno']
        data = Services.query.filter_by(sno=sno).first()
        data.service=name
        data.detail=detail
        db.session.commit()
        sno='0'
    elif request.method == 'POST' and 'Delete' in request.form:
        sno = session['sno']

        data = Services.query.filter_by(sno=sno).first()
        db.session.delete(data)
        db.session.commit()
        return redirect('/admin_services/0')

    elif sno!='0':
        data = Services.query.filter_by(sno=sno).first()
        print(sno)
        print(data)
        name = data.service
        detail = data.detail
        session['sno'] = sno

    li=[sno,name,detail]
    data =Services.query.all()

    return render_template('user/admin/admin_services.html', data=data,li=li)


@app.route('/user_service',methods=['GET', 'POST'])
def user_service():
    service = ' '
    name= ' '
    email = ' '
    if request.method == 'POST':
        service=request.form.get('service')
        detail = request.form.get('detail')
        slot = request.form.get('slot')
        date = request.form.get('date')

        name=session['name']
        email=session['uid']

        entry = Requests(username=name, email=email, service=service,detail=detail,date=date,slot=slot)
        db.session.add(entry)
        db.session.commit()


    data=Services.query.all()

    return render_template('user/client/user_service.html',data=data)

@app.route('/requests/<string:sno>',methods=['GET', 'POST'])
def requests(sno):
    service = ' '
    name = ' '
    email = ' '
    reply=''
    date = ''
    slot= ' '
    detail = ''

    if request.method == 'POST' and 'Reply' in request.form:
        reply = request.form.get('reply')
        email = request.form.get('email')
        name = request.form.get('name')
        entry = Reply(name=name, username=email, reply=reply)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('Message from ' + "eLearning",
                          sender=params['email'],
                          recipients=[email],
                          body="Hello " + name + "\n " + reply)
        sno='0'

    elif request.method == 'POST' and 'Delete' in request.form:
        data = Requests.query.filter_by(sno=sno).first()
        db.session.delete(data)
        db.session.commit()

        return redirect('/requests/0')

    elif sno!='0':
        data = Requests.query.filter_by(sno=sno).first()
        name = data.username
        email = data.email
        service = data.service
        date=data.date
        slot=data.slot
        detail=data.detail


    li = [sno,name,email,service,detail,date,slot]
    data=Requests.query.all()
    return render_template('user/admin/requests.html', data=data, li=li)

@app.route('/reply/<string:sno>',methods=['GET', 'POST'])
def reply(sno):
    date=''
    reply=''

    email=session['uid']

    if sno!='0':
        data = Reply.query.filter_by(sno=sno).first()
        reply=data.reply




    li = [sno,date,reply]
    data=Reply.query.filter_by(username=email).order_by(desc(Reply.sno))
    return render_template('user/client/user_reply.html', data=data, li=li)


@app.route('/my_request/<string:sno>',methods=['GET', 'POST'])
def my_request(sno):
    email=session['uid']
    service = ' '
    name = ' '
    reply = ''
    date = ''
    slot = ' '
    detail = ''

    if request.method == 'POST' and 'Modify' in request.form:
        data=Requests.query.filter_by(sno=sno).first()
        name=request.form.get('name')
        service=request.form.get('service')
        detail=request.form.get('det')
        date=request.form.get('date')
        slot=request.form.get('slot')
        data.status='1'
        db.session.commit()

        entry = Requests(username=name,email=email,service=service,detail=detail,date=date,slot=slot)
        db.session.add(entry)
        db.session.commit()

        return redirect('/my_request/0')

    elif request.method == 'POST' and 'Cancel' in request.form:
        data = Requests.query.filter_by(sno=sno).first()
        data.status = '2'
        db.session.commit()
        return redirect('/my_request/0')
    if sno != '0':
        data = Requests.query.filter_by(sno=sno).first()
        service = data.service
        date = data.date
        slot = data.slot
        detail = data.detail
        name=data.username

    li = [sno,service,detail,date,slot,name]
    data = Requests.query.filter_by(email=email).order_by(desc(Requests.sno))
    return render_template('user/client/my_request.html', data=data, li=li)

@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    name = ""
    email = ""
    cno = ""
    add=""
    plan = ""
    date = ""
    today =""
    date1= ""
    if request.method == 'POST':
        sno = session['id']
        data = Member.query.filter_by(sno=sno).first()
        sno=session['id']
        data.name=name
        data.email=email
        data.contact=cno
        data.address=add
        db.session.commit()
        msg="Profile Updated successfully"

    else:
        sno = session['id']
        data = Member.query.filter_by(sno=sno).first()

        name = data.name
        email = data.email
        cno = data.contact
        add = data.address
        data2 = Member_service.query.filter_by(mid=session['id']).order_by(desc(Member_service.sno)).first()
        date1 = data2.date
        duration = data2.plan
        if duration == '6 months':
            day = 180
        elif duration == '12 months':
            day = 365
        elif duration == '18 months':
            day = 540
        elif duration == '24 months':
            day = 730
        date1 = date1[:10]

        from datetime import date
        y = int(date1[0:4])
        m = int(date1[5:7])
        d = int(date1[8:10])
        a = date(y, m, d) + timedelta(days=day)
        print(a)
        today = datetime.now()
        today = datetime.strftime(today, "%Y-%m-%d")
        y1 = int(today[0:4])
        m1 = int(today[5:7])
        d1 = int(today[8:10])
        b = date(y1, m1, d1)
        rem = a - b
        rem = str(rem)
        final = ""
        final = rem.split()[0]
        final = int(final)
        if final<=0:
            final=0

    li = [sno, name, email, cno, add, final]
    return render_template('user/client/user_profile.html',li=li)

@app.route('/renew/<string:sno>', methods=['GET', 'POST'])
def renew(sno):
    plan = ''
    bank = ''
    dd = ''
    if request.method == 'POST':
        plan = request.form.get('plan')
        bank = request.form.get('bank')
        dd = request.form.get('dd')
        entry = Member_service(mid=sno, email=session['uid'], bank=bank,dd=dd,plan=plan)
        db.session.add(entry)
        db.session.commit()
        from datetime import date
        today = datetime.now()
        today = datetime.strftime(today, "%Y-%m-%d")
        y1 = int(today[0:4])
        m1 = int(today[5:7])
        d1 = int(today[8:10])
        b = date(y1, m1, d1)
       # rem = str(rem)
        final = ""
       # final = rem.split()[0]
        final = int(final)


    return render_template('user/client/renew.html')

if __name__ == '__main__':
    app.run(debug=True)