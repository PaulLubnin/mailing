import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

gmail_smpt = "smtp.gmail.com"
gmail_imap = "imap.gmail.com"
port = 587


class SendMail:
    def __init__(self, login, password, recipients, message, subject='Subject', header=None):
        self.login = login
        self.password = password
        self.subject = subject
        self.recipients = recipients
        self.message = message
        self.header = header

    def send_mail(self):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(self.recipients)
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.message))
        server = smtplib.SMTP(gmail_smpt, port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.login, self.password)
        server.sendmail(self.login, self.recipients, msg.as_string())
        server.quit()
        return

    def receiving_mail(self):
        mail = imaplib.IMAP4_SSL(gmail_imap)
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
        print(email_message)
        mail.logout()
        return


def get_recipient_list(input_recipient_list):
    recipient_list = input_recipient_list.split(', ')
    return recipient_list


if __name__ == '__main__':
    print('Скрипт для отправки/получения почты (работает с gmail)')
    print('Для создания рассылки и получения писем введите необходимые данные ')
    login = input('Введите email с которого будет рассылка ')
    password = input('Введите пароль от почты ')
    # subject = 'Subject'
    recipients = get_recipient_list(input('Введите адреса получателей через запятую '))
    message = (input('Введите текст сообщения '))
    # header = None
    mailing = SendMail(login, password, recipients, message)
    print('Доступные команды:\n'
          '"s" - отправить письмо\n'
          '"r" - получить письмо\n'
          '"q" - выход\n')
    input_command = input('Введите команду ')
    if input_command == "s":
        mailing.send_mail()
        print('Письмо отправлено')
    if input_command == "r":
        mailing.receiving_mail()
        print('Письмо получено')
