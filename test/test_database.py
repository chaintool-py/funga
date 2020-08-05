#!/usr/bin/python

import unittest
import logging
import base64

import psycopg2
from psycopg2 import sql
from cryptography.fernet import Fernet, InvalidToken

from keystore import ReferenceDatabase

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestDatabase(unittest.TestCase):

    conn = None
    cur = None
    symkey = None
    address_hex = None
    db = None

    def setUp(self):
        # arbitrary value
        symkey_hex = 'E92431CAEE69313A7BE9E443C4ABEED9BF8157E9A13553B4D5D6E7D51B5021D9'
        self.symkey = bytes.fromhex(symkey_hex)
        self.address_hex = '9FA61f0E52A5C51b43f0d32404625BC436bb7041'

        kw = {
                'symmetric_key': self.symkey,
                }
        self.db = ReferenceDatabase('signer_test', **kw)
        self.db.cur.execute("""CREATE TABLE ethereum (
        id SERIAL NOT NULL PRIMARY KEY,
        key_ciphertext VARCHAR(256) NOT NULL,
        wallet_address_hex CHAR(40) NOT NULL
        );
""")
        self.db.cur.execute("CREATE UNIQUE INDEX ethereum_address_idx ON ethereum ( wallet_address_hex );")
        self.db.conn.commit()
        self.db.new(self.address_hex, 'foo')


    def tearDown(self):
        self.db.conn = psycopg2.connect('dbname=signer_test')
        self.db.cur = self.db.conn.cursor()
        self.db.cur.execute('DROP INDEX ethereum_address_idx;')
        self.db.cur.execute('DROP TABLE ethereum;')
        self.db.conn.commit()


    def test_get_key(self):
        self.db.get(self.address_hex, 'foo')
        with self.assertRaises(InvalidToken):
           self.db.get(self.address_hex, 'bar')


if __name__ == '__main__':
    unittest.main()
