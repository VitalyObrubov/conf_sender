import os
import smtplib

from email.utils import formatdate, make_msgid
from email.message import EmailMessage
# For guessing MIME type based on file name extension
import mimetypes

from app.globals import MyApp
from app.message import MESS1,MESS2,MESS3, MESS_TXT

def send_email(app: MyApp, to_addr, subject, file_to_attach, cc_addr, user):
    """
    Отправка электронного письма с вложением
    """

    # извлечение переменных из конфигурации
    server = app.config.email.email_host
    port = app.config.email.email_port
    from_addr = app.config.email.email_host_user
    passwd = app.config.email.email_host_password
    # формируем тело письма
    msg = EmailMessage()
    msg["From"] = from_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)

    msg["To"] = ', '.join(to_addr)
    msg["cc"] = ', '.join(cc_addr)
    emails = to_addr + cc_addr

    msg.set_content(MESS_TXT)

    img_cid = make_msgid()
     
    msgText = MESS1+user+MESS2+str(img_cid[1:-1])+MESS3
    msg.add_alternative(msgText, subtype='html')

    img_file = os.path.join("temp/" + file_to_attach + ".png")
    with open(img_file, "rb") as img:
        # know the Content-Type of the image
        maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')
        # attach it
        payload = msg.get_payload()
        payload[1].add_related(img.read(), 
                                    maintype=maintype, 
                                    subtype=subtype, 
                                    cid=img_cid,
                                    filename = file_to_attach + ".png")

    conf_cid = make_msgid()
    conf_file = os.path.join("temp/" + file_to_attach + ".conf")
    with open(conf_file, "rb") as conf:
        payload = msg.get_payload()
        payload[1].add_related(conf.read(), 
                                    maintype='application', 
                                    subtype='octet-stream', 
                                    cid=conf_cid,
                                    filename = file_to_attach + ".conf")        


    try:
        smtp = smtplib.SMTP_SSL(server, port)
        smtp.ehlo()
        res = smtp.login(from_addr, passwd)
        res = smtp.sendmail(from_addr, emails, msg.as_string())
    except smtplib.SMTPException as err:
        print('Что - то пошло не так...')
        raise err
    finally:
        smtp.quit()


