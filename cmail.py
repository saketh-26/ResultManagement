import smtplib
from email.message import EmailMessage
def sendmail(to,subject,body):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('sakethreddy.kallepu@gmail.com','sbbs bhfc onhg ctfh')
    msg=EmailMessage()
    msg['From']='sakethreddy.kallepu@gmail.com'
    msg['Subject']=subject
    msg['To']=to
    msg.set_content(body)
    server.send_message(msg)
    server.quit()


