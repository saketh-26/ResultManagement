from flask import Flask,redirect,render_template,url_for,request,jsonify,flash,abort
from flask_mysqldb import MySQL
from flask_session import Session
from key import *
from cmail import sendmail
from stoken import token
from itsdangerous import URLSafeTimedSerializer
 
app=Flask(__name__)
app.secret_key=secret_key
app.config['SESSION_TYPE']='filesystem'
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='result'
mysql=MySQL(app)

@app.route('/')
def welcome():
    return render_template('welcomepage.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

'''@app.route('/student',methods=['GET','POST'])
def student():
    if request.method=='POST':
        student=request.form['student']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * from marks where stud_id=%s',[student])
        data=cursor.fetchall()
        cursor.close()
        if len(data)==0:
            return 'No data Found'
        else:
            return render_template('finalcertificate.html',data=data)
    return render_template('student.html')'''
@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        student_id = request.form['student']
        cursor = mysql.connection.cursor()

        # Fetch marks data for the student
        cursor.execute('SELECT * from marks where stud_id=%s', [student_id])
        data = cursor.fetchall()

        # Calculate total marks, percentage, grade, and pass/fail for each subject
        result_data = []
        for row in data:
            subject = row[1]
            obtained_marks = row[2]
            total_marks = get_total_marks(subject)  # Assuming a function to get total marks for a subject

            percentage = (obtained_marks / total_marks) * 100
            grade = calculate_grade(percentage)  # Assuming a function to calculate grade based on percentage
            pass_status = 'Pass' if percentage >= 40 else 'Fail'

            result_data.append((student_id,subject, obtained_marks, total_marks, percentage, grade, pass_status))

        cursor.close()

        if len(result_data) == 0:
            return 'No data Found'
        else:
            return render_template('finalcertificate.html', data=result_data)
    return render_template('student.html')
'''def get_total_marks(subject):
    # Define a dictionary to store total marks for each subject
    subject_total_marks = {
        'Mathematics': 100,
        'Science': 100,
        'English': 100,
        # Add more subjects as needed
    }

    # Return total marks for the subject if found, otherwise return a default value
    return subject_total_marks.get(subject, 100)  # Default value is 100 if subject is not found'''
def get_total_marks(subject):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT total_marks FROM subjects WHERE subject=%s', [subject])
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result[0]
    else:
        return 100  # Default value if subject not found or total marks not available
def calculate_grade(percentage):
    # Define grade ranges and corresponding grades
    grade_ranges = {
        (90, 100): 'A+',
        (80, 89): 'A',
        (70, 79): 'B',
        (60, 69): 'C',
        (50, 59): 'D',
        (40, 49): 'E',
        (0, 39): 'F',
    }

    # Iterate through grade ranges and return the corresponding grade
    for range_, grade in grade_ranges.items():
        if percentage >= range_[0] and percentage <= range_[1]:
            return grade

    return 'Unknown'  # Return 'Unknown' if percentage is outside defined ranges


@app.route('/finalcertificate',methods=['GET','POST'])
def final():
    if request.method=='POST':
        student=request.form['student']
        cursor=mysql.connection.cursor()    
        cursor.execute("SELECT count(*) from marks where stud_id=%s",[student])
        count=int(cursor.fetchone()[0])
        cursor.close()
        if count==0:
            return render_template('final.html',student='empty')
        else:
            cursor=mysql.connection.cursor()    
            cursor.execute("SELECT * from marks where stud_id=%s",[student])
            count=cursor.fetchall()
            cursor.close()
            return render_template('final.html',student=count)
    return render_template('final.html')

@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    if request.method=='POST':
        user=request.form['userName']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT userName,password from admin where userName=%s',[user])
        data=cursor.fetchall()[0]
        user=data[0]
        password=data[1]
        cursor.close()
        if user==user and password==password:
            return redirect(url_for('addstudents'))
        else:
            return render_template('adminlogin.html')
    return render_template('adminlogin.html')
@app.route('/signin',methods=['GET','POST'])
def signin():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT count(*) from admin')
    result=int(cursor.fetchone()[0])
    if request.method=='POST':
        username=request.form['user']
        email=request.form['mail']
        number=request.form['phone']
        password=request.form['password']
        passcode=request.form['passcode']
        gender=request.form['gender']
        cursor.execute('select count(*) from admin where userName=%s',[username])
        count=cursor.fetchone()[0]
        cursor.execute('select count(*) from admin where email=%s',[email])
        count1=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            flash('username already in use')
            return render_template('signin.html')
        elif count1==1:
            flash('Email already in use')
            return render_template('signin.html')
        data={'username':username,'password':password,'email':email,'number':number,'passcode':passcode,'gender':gender}
        subject='Email Confirmation'
        body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('confirm',token=token(data,salt),_external=True)}"
        sendmail(to=email,subject=subject,body=body)
        flash('Confirmation link sent to mail')
        return redirect(url_for('adminlogin'))
        ''' otp=genotp()
        subject='Thanks for registering'
        body = 'your one time password is- '+otp
        sendmail(email,subject,body)
        return render_template('otp.html',otp=otp,key=key,name=name,username=username,email=email,number=number,password=password,passcode=passcode,gender=gender)
        cursor=mysql.connection.cursor()
        cursor.execute('insert into admin values(%s,%s,%s,%s,%s,%s,%s,%s)',[key,name,username,email,number,password,passcode,gender])
        mysql.connection.commit()'''
                 
    return render_template('signin.html')

'''@app.route('/otp/<otp>/<key>/<name>/<username>/<email>/<number>/<password>/<passcode>/<gender>',methods=['POST','GET'])
def getotp(otp,key,name,username,email,number,password,passcode,gender):
    if request.method == 'POST':
        OTP=request.form['otp']
        if otp == OTP:
            cursor=mysql.connection.cursor() 
            cursor.execute('insert into admin values(%s,%s,%s,%s,%s,%s,%s)',[username,email,number,password,passcode,gender])
            mysql.connection.commit()
            cursor.close()
            flash('Details registered successfully')
            return redirect(url_for('adminlogin'))
        else:
            flash('wrong OTP')

    return render_template('otp.html',otp=otp,key=key,name=name,username=username,email=email,number=number,password=password,passcode=passcode,gender=gender)'''
@app.route('/confirm/<token>')
def confirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
        #print(e)
        return 'Link Expired register again'
    else:
        cursor=mysql.connection.cursor() 
        username=data['username']
        cursor.execute('select count(*) from admin where userName=%s',[username])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('adminlogin'))
        else:
            cursor.execute('insert into admin values(%s,%s,%s,%s,%s,%s)',[data['username'],data['email'],data['number'],data['password'],data['passcode'],data['gender']])
            mysql.connection.commit()
            cursor.close()
            flash('Details registered!')
            return redirect(url_for('adminlogin'))

'''@app.route('/forgotpassword',methods=('GET', 'POST'))
def forgotpassword():
    if request.method=='POST':
        username = request.form['name']
        cursor=mysql.connection.cursor() 
        cursor.execute('select userName from admin') 
        deta=cursor.fetchall()
        print(deta)
        if (username,) in deta:
            cursor.execute('select email from admin where userName=%s',[username])
            data=cursor.fetchone()[0]
            cursor.close()
            subject=f'Reset Password for {data}'
            body=f'Reset the passwword using-\{request.host+url_for("resetpwd",token=token(username,300))}'
            sendmail(data,subject,body)
            flash('Reset link sent to your registered mail id')
            return redirect(url_for('adminlogin'))
        else:
            flash('user does not exits')
    return render_template('forgot.html')

@app.route('/resetpwd/<token>',methods=('GET', 'POST'))
def resetpwd(token):
    try:
        s=Serializer(app.config['SECRET_KEY'])
        username=s.loads(token)['user']
        if request.method=='POST':
            npwd = request.form['npassword']
            cpwd = request.form['cpassword']
            if npwd == cpwd:
                cursor=mysql.connection.cursor()
                cursor.execute('update admin set password=%s where userName=%s',[npwd,username])
                mysql.connection.commit()
                cursor.close()
                return 'Password reset Successfull'
            else:
                return 'Password does not matched try again'
        return render_template('newpassword.html')
    except Exception as e:
        abort(410,description='reset link expired')'''

@app.route('/forget',methods=['GET','POST'])
def forgot():
    if request.method=='POST':
        email=request.form['email']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from admin where email=%s',[email])
        count=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            cursor=mysql.connection.cursor()
            cursor.execute('SELECT email from admin where email=%s',[email])
            status=cursor.fetchone()[0]
            cursor.close()
            subject='Forget Password'
            confirm_link=url_for('reset',token=token(email,salt=salt2),_external=True)
            body=f"Use this link to reset your password-\n\n{confirm_link}"
            sendmail(to=email,body=body,subject=subject)
            flash('Reset link sent check your email')
            return redirect(url_for('adminlogin'))
        else:
            flash('Invalid email id')
            return render_template('forgot.html')
    return render_template('forgot.html')


@app.route('/reset/<token>',methods=['GET','POST'])
def reset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        email=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['npassword']
            confirmpassword=request.form['cpassword']
            if newpassword==confirmpassword:
                cursor=mysql.connection.cursor()
                cursor.execute('update admin set password=%s where email=%s',[newpassword,email])
                mysql.connection.commit()
                flash('Reset Successful')
                return redirect(url_for('adminlogin'))
            else:
                flash('Passwords mismatched')
                return render_template('newpassword.html')
        return render_template('newpassword.html')


@app.route('/addstudents',methods=['GET','POST'])
def addstudents():
    if request.method=='POST':
        studentId=request.form['studentId']
        studentName=request.form['studentName']
        fatherName=request.form['fatherName']
        motherName=request.form['motherName']
        phoneNumber=request.form['phoneNumber']
        address=request.form['address']
        emailId=request.form['emailId']
        adharNumber=request.form['adharNumber']
        gender=request.form['gender']
        section=request.form['section']
        cursor=mysql.connection.cursor()
        cursor.execute('insert into students(studentId,studentName,fatherName,motherName,phoneNumber,address,emailId,adharNumber,gender,section) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[studentId,studentName,fatherName,motherName,phoneNumber,address,emailId,adharNumber,gender,section])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('addsubjects'))
    return render_template('addstudents.html')

@app.route('/addsubjects',methods=['GET','POST'])
def addsubjects():
    if request.method=='POST':
        section=request.form['section']
        courseid=request.form['course']
        subjectName=request.form['subjectName']
        totalMarks=request.form['totalMarks']
        cursor=mysql.connection.cursor()
        #query=f"insert into {section} (subject,total_marks) values('{subjectName}',{totalMarks})"
        cursor.execute('insert into subjects(section,course_id,subject,total_marks) values(%s,%s,%s,%s)',[section,courseid,subjectName,totalMarks])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('addresult'))
    return render_template('addsubjects.html')

@app.route('/addresult',methods=['GET','POST'])
def addresult():
    cursor=mysql.connection.cursor()
    cursor.execute('select subject from subjects')
    data=cursor.fetchall()
    subjects=data 
    if request.method=='POST':
        studentId=request.form['student']
        subject=request.form['subject']
        obtainedMarks=request.form['obtained']
        cursor=mysql.connection.cursor()
        cursor.execute('insert into marks(stud_id,subject,obtained) values(%s,%s,%s)',[studentId,subject,obtainedMarks])
        mysql.connection.commit()
        cursor.close()
        return render_template('addresult.html' ,subjects=subjects)
    return render_template('addresult.html',subjects=subjects)

@app.route('/viewstudent',methods=['GET','POST'])
def viewstudent():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from students')
    students=cursor.fetchall()
    cursor.close()
    return render_template('viewstudent.html',students=students)

@app.route('/studentsearch',methods=['POST'])
def studentsearch():
    if request.method=='POST':
        students=request.form['studentId']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from students where studentId=%s',[students])
        count=int(cursor.fetchone()[0])
        cursor.close()
        if count==0:
            return render_template('searchbar_students.html',students='empty')
        else:
            cursor=mysql.connection.cursor()
            cursor.execute('select * from students where studentId=%s',[students])
            count=cursor.fetchall()
            cursor.close()
            return render_template('searchbar_students.html',students=count)
    return render_template('searchbar_students.html',students=count)

@app.route('/deletestudent',methods=['POST'])
def deletestudent():
    if request.method=='POST':
        print(request.form)
        student=request.form['option'].split()
        cursor=mysql.connection.cursor()
        cursor.execute('delete from students where studentId=%s',[student[0]])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('viewstudent'))
    
@app.route('/viewsubject')
def viewsubject():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * from subjects")
    subjects=cursor.fetchall()
    cursor.close()
    return render_template('viewsubject.html',subjects=subjects)


@app.route('/subjectsearch',methods=['POST'])
def subjectsearch():
    if request.method=='POST':
        subjects=request.form['course']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from subjects where course_id=%s',[subjects])
        count=int(cursor.fetchone()[0])
        cursor.close()
        if count==0:
            return render_template('searchbar_subject.html',subjects='empty')
        else:
            cursor=mysql.connection.cursor()
            cursor.execute('select * from subjects where course_id=%s',[subjects])
            count=cursor.fetchall()
            cursor.close()
            return render_template('searchbar_subject.html',subjects=count)
    return render_template('searchbar_subject.html')

@app.route('/deletesubject',methods=['POST'])
def deletesubject():
    if request.method=='POST':
        print(request.form)
        course=request.form['option1'].split()
        cursor=mysql.connection.cursor()
        cursor.execute('delete from subjects where course_id=%s',[course[0]])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('viewsubject'))
        
@app.route('/viewresult',methods=['GET','POST'])
def viewresult():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from marks')
    marks=cursor.fetchall()
    cursor.close()
    return render_template('viewresult.html',marks=marks)

@app.route('/resultsearch',methods=['POST'])
def resultsearch():
    if request.method=='POST':
        marks=request.form['studentId']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from marks where stud_id=%s',[marks])
        count=int(cursor.fetchone()[0])
        cursor.close()
        if count==0:
            return render_template('searchbar_result.html',marks='empty')
        else:
            cursor=mysql.connection.cursor()
            cursor.execute('SELECT * from marks where stud_id=%s',[marks])
            count=cursor.fetchall()
            cursor.close()
            return render_template('searchbar_result.html',marks=count)
        return render_template('searchbar_result.html')
        
@app.route('/deleteresult',methods=['POST'])
def deleteresult():
    if request.method=='POST':
        print(request.form)
        result=request.form['option2'].split()
        cursor=mysql.connection.cursor()
        cursor.execute('delete from marks where stud_id=%s',[result[0]])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('viewresult'))


app.run(debug=True)
