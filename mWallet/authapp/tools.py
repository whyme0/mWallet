from authapp.models import Token

import time
import threading


def is_token_exist(token):
    try:
        Token.objects.get(token=token)
        return True
    except Token.DoesNotExist:
        return False


def start_token_delete(token):
    '''
    Create new thread that waiting 3.5 minutes
    and then delete Token object of particular user.
    '''

    def target_func():
        print('New thread started.')
        time.sleep(210)
        try:
            Token.objects.get(token=token).delete()
            print('Token deleted.')
        # if token already deleted than just ignore.
        except Token.DoesNotExist:
            pass

    thread = threading.Thread(target=target_func)
    thread.start()
