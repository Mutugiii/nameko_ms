import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from string import Template
from nameko.rpc import rpc


mail_server = os.environ.get('MAIL_SERVER')
mail_port = os.environ.get('MAIL_PORT')
mail_username = os.environ.get('MAIL_USERNAME')
mail_password = os.environ.get('MAIL_PASSWORD')
    

def read_template(filename):
    ''' Returns a template object that the email can send'''
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


class MailerService:
    name = "mailer_service"

    @rpc
    def create(self, receiver_email, receiver_name, mail_message):
        # Setup the smtp server
        server = smtplib.SMTP(host=mail_server, port=mail_port)
        server.starttls()
        server.login(mail_username, mail_password)

        message = MIMEMultipart("alternative")
        message["Subject"] = "HNGi7"
        message["From"] = mail_username
        message["To"] = receiver_email
        message_text = read_template('/templates/mail_message.txt')
        message_html = read_template('/templates/mail_message.html')

        messagetext = message_text.substitute(PERSON_NAME=receiver_name, MAIL_MESSAGE=mail_message)
        messagehtml = message_html.substitute(PERSON_NAME=receiver_name, MAIL_MESSAGE=mail_message)

        part1 = MIMEText(messagetext, "plain")
        part2 = MIMEText(messagehtml, "html")

        message.attach(part1)
        message.attach(part2)

        server.send_message(message)
        del message

        server.quit()
        return 'Sent to email {}'.format(receiver_email)
