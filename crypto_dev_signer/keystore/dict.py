# standard imports
import logging

# external imports
from hexathon import (
        strip_0x,
        add_0x,
        )

# local imports
#from . import keyapi
from .interface import Keystore
from crypto_dev_signer.error import UnknownAccountError
from crypto_dev_signer.encoding import private_key_to_address

logg = logging.getLogger()


class DictKeystore(Keystore):

    def __init__(self):
        self.keys = {}


    def get(self, address, password=None):
        address_key = strip_0x(address).lower()
        if password != None:
            logg.debug('password ignored as dictkeystore doesnt do encryption')
        try:
            return self.keys[address_key]
        except KeyError:
            raise UnknownAccountError(address_key)


    def list(self):
        return list(self.keys.keys())


    def import_key(self, pk, password=None):
        address_hex = private_key_to_address(pk)
        address_hex_clean = strip_0x(address_hex).lower()
        self.keys[address_hex_clean] = pk.secret
        logg.debug('added key {}'.format(address_hex))
        return add_0x(address_hex)
