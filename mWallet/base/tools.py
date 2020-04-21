# bult-in libraries
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint

# installed packages
import requests
from django.conf import settings
from django.contrib import messages

# local libraries
from unpublic import security

chars = [
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z',
    'x', 'c', 'v', 'b', 'n', 'm', '1', '2', '3', '4',
    '5', '6', '7', '8', '9', '0', '@', '#', '%', '^',
    '(', '*', ')', '[', ']', '{', '}',
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
    str_ = ''
    for i in range(length):
        str_ += chrs_[randint(0, len(chrs_)-1)]

    return str_


def send_yandex_email(from_, subject, message, files=None):
    from_addr = security.YA_EMAIL
    to_addr = from_addr
    password = security.YA_PASSWORD

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


def check_captcha(function):
    def wrap(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': security.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post(
                'https://www.google.com/recaptcha/api/siteverify',
                data=data,
            )
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
