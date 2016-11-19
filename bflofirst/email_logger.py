import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import datetime

def send_mail(send_from, send_to, subject, text, files=None,
              server="smtp.gmail.com"):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)


    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login('naterautologger@gmail.com','margaglio22')
    server.sendmail(send_from, send_to, msg.as_string())
    server.close()

def send_log(log_info=""):
    send_mail('naterautologger@gmail.com', ['nathanmargaglio@gmail.com'], 'Log: ' + str(datetime.datetime.now()), log_info, ['log.png'])
