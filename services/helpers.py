import datetime
from base64 import b32encode
from hashlib import sha1
from random import random
from random import randint


def dateNow():
    return datetime.datetime.now() + datetime.timedelta(hours=2)


def pkgen():
    return b32encode(sha1(str(random())).digest()).lower()[:12]


def rand_int():
    return randint(-9999999, 9999999)
