import time
import secrets


class CsrfImpl(object):
    def __init__(self, key_length):
        self.key_length = key_length

    def gen_token(self):
        token = secrets.token_hex(self.key_length)
        return token

