# bult-in libraries
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint

# local libraries
from unpublic import security
from authapp.models import Token
from accounts.models import Person

chars = [
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z',
    'x', 'c', 'v', 'b', 'n', 'm', '1', '2', '3', '4',
    '5', '6', '7', '8', '9', '0',
]


def shuffle(arr, n):
    '''
    The function returns a mixed list
    '''
    for i in range(0, n):
        for _ in range(len(arr)):
            index1 = _
            index2 = randint(0, len(arr) - 1)

            value = arr[index1]

            arr[index1] = arr[index2]
            arr[index2] = value

    return arr


def get_random_key(length=20):
    '''
    Generate random key like set of chars as string
    and return this key.
    '''
    chrs_ = shuffle(chars, 30)
    token = ''

    active_tokens = []
    while True:
        # creating token
        for i in range(length):
            token += chrs_[randint(0, len(chrs_) - 1)]

        if token not in active_tokens:
            try:
                Token.objects.get(token=token)
                active_tokens.append(token)

            # if such token doesn't exist yet, then return it
            except Token.DoesNotExist:
                return token


def send_yandex_email(email, subject, message, files=None):
    from_addr = security.YA_EMAIL
    to_addr = email
    password = security.YA_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    message = """\
    From: {0}

    ______________
    Body: {1}
    """.format(email, message)
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(from_addr, password)
    server.send_message(msg)
    server.quit()


def is_email_exist(email):
    try:
        Person.objects.get(email=email)
        return True
    except Person.DoesNotExist:
        return False
