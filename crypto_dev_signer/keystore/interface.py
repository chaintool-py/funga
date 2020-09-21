# standard imports
import os

# local imports
from . import keyapi


class Keystore:

    def get(self, address, password=None):
        raise NotImplementedError


    def new(self, password=None):
        b = os.urandom(32)
        return self.import_raw_key(b, password)


    def import_raw_key(self, b, password=None):
        pk = keyapi.PrivateKey(b)
        return self.import_key(pk, password)


    def import_key(self, pk, password=None):
        raise NotImplementedError


    def insert_key(self, pk, password=None):
        raise NotImplementedError

