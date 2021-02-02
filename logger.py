from os import environ
from time import gmtime, asctime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def log_this(function):
    def inner(message, *args, **kwargs):
        log(message)
        function(message, *args, **kwargs)
    return inner


def log(message):
    print(message.text)
    with open('log.log', 'a') as file:
        file.write(create_log_str(message) + '\n')


def create_log_str(message):
    date = message.date
    date = '{}.{}.{} {}:{}:{}'.format(str(gmtime(date).tm_mday).rjust(2, '0'), str(gmtime(date).tm_mon).rjust(2, '0'),
                                      str(gmtime(date).tm_year).rjust(2, '0'), str(gmtime(date).tm_hour).rjust(2, '0'),
                                      str(gmtime(date).tm_min).rjust(2, '0'), str(gmtime(date).tm_sec).rjust(2, '0'))

    log_str = 'message_id:{}|date:{}|used_id:{}|username:{}|first_name:{}|last_name:{}|text:{}'.format(
        message.message_id, date, message.from_user.id, message.from_user.username,
        message.from_user.first_name, message.from_user.last_name, message.text
    )
    return log_str


def send_mail(message):
    email = 'denisov_aa@gkl-kemerovo.ru'
    password = environ.get('PASSWORD_SHIT')
    mail_account = smtplib.SMTP('smtp.gmail.com', 587)
    mail_account.starttls()
    mail_account.login(user=email, password=password)

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = f'Logging. {message.from_user.username} {message.from_user.first_name} {message.from_user.last_name} sent a message to the SHIT bot!'
    text_message = create_log_str(message)
    msg.attach(MIMEText(text_message, 'plain'))
    mail_account.send_message(from_addr=email, to_addrs=msg['To'], msg=msg)
    mail_account.quit()
