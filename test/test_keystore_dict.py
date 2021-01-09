#!/usr/bin/python

# standard imports
import unittest
import logging
import base64
import os

# third-party imports
import psycopg2
from psycopg2 import sql
from cryptography.fernet import Fernet, InvalidToken

# local imports
from crypto_dev_signer.keystore import DictKeystore
from crypto_dev_signer.error import UnknownAccountError

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

script_dir = os.path.realpath(os.path.dirname(__file__))


class TestDatabase(unittest.TestCase):

    conn = None
    cur = None
    symkey = None
    address_hex = None
    db = None

    def setUp(self):
        logg.debug('setup')
        # arbitrary value
        #symkey_hex = 'E92431CAEE69313A7BE9E443C4ABEED9BF8157E9A13553B4D5D6E7D51B5021D9'
        #self.symkey = bytes.fromhex(symkey_hex)

        #kw = {
        #        'symmetric_key': self.symkey,
        #        }
        self.db = DictKeystore()

        keystore_filepath = os.path.join(script_dir, 'testdata', 'UTC--2021-01-08T18-37-01.187235289Z--00a329c0648769a73afac7f9381e08fb43dbea72')
        #f = open(
        #s = f.read()
        #f.close()

        self.address_hex = self.db.import_keystore_file(keystore_filepath, '')[2:]


    def tearDown(self): 
        pass


    def test_get_key(self):
        logg.debug('getting {}'.format(self.address_hex))
        pk = self.db.get(self.address_hex, '')

        self.assertEqual(pk.public_key.to_checksum_address()[2:], self.address_hex)

        bogus_account = os.urandom(20).hex()
        with self.assertRaises(UnknownAccountError):
           self.db.get(bogus_account, '')


if __name__ == '__main__':
    unittest.main()
