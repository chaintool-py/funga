#!/usr/bin/python

# standard imports
import unittest
import logging
import base64
import os

# external imports
from hexathon import (
    strip_0x,
    add_0x,
    )

# local imports
from funga.error import UnknownAccountError
from funga.eth.keystore.dict import DictKeystore
from funga.eth.signer import EIP155Signer

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

script_dir = os.path.realpath(os.path.dirname(__file__))


class TestDict(unittest.TestCase):

    address_hex = None
    db = None

    def setUp(self):
        self.db = DictKeystore()

        keystore_filepath = os.path.join(script_dir, 'testdata', 'UTC--2021-01-08T18-37-01.187235289Z--00a329c0648769a73afac7f9381e08fb43dbea72')

        address_hex = self.db.import_keystore_file(keystore_filepath, '')
        self.address_hex = add_0x(address_hex)


    def tearDown(self): 
        pass


    def test_get_key(self):
        logg.debug('getting {}'.format(strip_0x(self.address_hex)))
        pk = self.db.get(strip_0x(self.address_hex), '')

        self.assertEqual(self.address_hex.lower(), '0x00a329c0648769a73afac7f9381e08fb43dbea72')

        bogus_account = os.urandom(20).hex()
        with self.assertRaises(UnknownAccountError):
           self.db.get(bogus_account, '')

    
    def test_sign_message(self):
        s = EIP155Signer(self.db)
        z = s.sign_ethereum_message(strip_0x(self.address_hex), b'foo')
        logg.debug('zzz {}'.format(str(z)))



if __name__ == '__main__':
    unittest.main()
