# Мы устроились на новую работу. Бывший сотрудник начал разрабатывать модуль для работы с почтой, но не успел доделать
# его. Код рабочий. Нужно только провести рефакторинг кода.

# Создать класс для работы с почтой;
# Создать методы для отправки и получения писем;
# Убрать "захардкоженный" код. Все значения должны определяться как аттрибуты класса, либо аргументы методов;
# Переменные должны быть названы по стандарту PEP8;
# Весь остальной код должен соответствовать стандарту PEP8;
# Класс должен инициализироваться в конструкции.
#   if __name__ == '__main__'

import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendMail:
    def __init__(self, login, password, recipients, message, subject='Subject', header=None):
        self.login = login
        self.password = password
        self.subject = subject
        self.recipients = recipients
        self.message = message
        self.header = header

    def send_mail(self):
        GMAIL_SMTP = "smtp.gmail.com"
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ' '.join(self.recipients)
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.message))
        server = smtplib.SMTP(GMAIL_SMTP, 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.login, self.password)
        server.sendmail(self.login, self.recipients, msg.as_string())
        server.quit()

    def receiving_mail(self):
        GMAIL_IMAP = "imap.gmail.com"
        mail = imaplib.IMAP4_SSL(GMAIL_IMAP)
        mail.login(self.login, self.password)
        mail.list()
        mail.select('inbox')

        if self.header:
            criterion = '(HEADER Subject "%s")' % self.header
        else:
            criterion = 'ALL'

        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        mail.logout()


def get_recipient_list(input_recipient_list):
    recipient_list = input_recipient_list.split(', ')
    return recipient_list

def get_message(input_message):
    text_message = input_message
    return text_message

def mailing_list_creation():
    print('Для создания рассылки и получения писем введите необходимые данные ')
    login = input('Введите email с которого будет рассылка ')
    password = input('Введите пароль от почты ')
    # subject = 'Subject'
    recipients = get_recipient_list(input('Введите адреса получателей через запятую '))
    message = get_message(input('Введите текст сообщения '))
    # header = None
    mailing = SendMail(login, password, recipients, message)
    input_command = input('отправить или получить?')
    input_command = input_command.capitalize()
    if input_command is 'отправить':
        mailing.send_mail()
    if input_command is 'получить':
        mailing.receiving_mail()
    return mailing


if __name__ == '__main__':
    mailing_list_creation()
