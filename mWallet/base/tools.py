import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint

chars = [
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z',
    'x', 'c', 'v', 'b', 'n', 'm', '1', '2', '3', '4',
    '5', '6', '7', '8', '9', '0', '@', '#', '%', '^',
    '(', '*', ')', '[', ']', '{', '}',
]


def shuffle(arr, n):
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
    str_ = ''
    for i in range(length):
        str_ += chars[randint(0, len(chars)-1)]

    return str_


def send_yandex_email(from_, subject, message, files=None):
    from_addr = 'fancydresscostume@yandex.com'
    to_addr = 'fancydresscostume@yandex.com'
    password = ')Gr;y)Sp}u[G(ZRu-<,=>Ep?Nt9Skys&Mc{dwL$>Hp;/9v,!wu'

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    message = """\
    From: {0}

    ______________
    Body: {1}
    """.format(from_, message)
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(from_addr, password)
    server.send_message(msg)
    server.quit()
