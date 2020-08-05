#!/usr/bin/python

import unittest
import logging
import base64

import psycopg2
from psycopg2 import sql
from cryptography.fernet import Fernet

from keystore import ReferenceDatabase

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestDatabase(unittest.TestCase):

    conn = None
    cur = None
    symkey = None
    addr = None
    db = None
    pk = None

    def setUp(self):
                # arbitrary value
        symk_hex = 'E92431CAEE69313A7BE9E443C4ABEED9BF8157E9A13553B4D5D6E7D51B5021D9'
        self.symkey = bytes.fromhex(symk_hex)
        f = Fernet(base64.b64encode(self.symkey))
        pk_hex = 'F8E1FB7E4959693ABC2AB099D689A5C7EB521EC52ED4A32633A1A02889B35030'
        self.pk = bytes.fromhex(pk_hex)
        pk_ciphertext = f.encrypt(self.pk)
        self.addr = '9FA61f0E52A5C51b43f0d32404625BC436bb7041'

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
        self.db.conn.commit()
        self.db.cur.execute("CREATE UNIQUE INDEX ethereum_address_idx ON ethereum ( wallet_address_hex );")

        self.db.cur.execute(
                sql.SQL('INSERT INTO ethereum (key_ciphertext, wallet_address_hex) VALUES (%s, %s)'),
                [
                    pk_ciphertext.decode('utf-8'),
                    self.addr,
                    ],
                )
        self.db.conn.commit()


    def tearDown(self):
        self.db.conn = psycopg2.connect('dbname=signer_test')
        self.db.cur = self.db.conn.cursor()
        self.db.cur.execute('DROP INDEX ethereum_address_idx;')
        self.db.cur.execute('DROP TABLE ethereum;')
        self.db.conn.commit()


    def test_get_key(self):
        pk = self.db.get(self.addr)
        self.assertEqual(self.pk, pk)


if __name__ == '__main__':
    unittest.main()
