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
