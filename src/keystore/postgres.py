import logging
import base64
import os

from cryptography.fernet import Fernet
import psycopg2
from psycopg2 import sql
from eth_keys import KeyAPI
from eth_keys.backends import NativeECCBackend
import sha3

from common import strip_hex_prefix

keyapi = KeyAPI(NativeECCBackend)

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger(__file__)



def to_bytes(x):
    return x.encode('utf-8')

    
class ReferenceDatabase:


        def __init__(self, dbname, **kwargs):
            self.conn = psycopg2.connect('dbname=' + dbname)
            self.cur = self.conn.cursor()
            self.symmetric_key = kwargs.get('symmetric_key')


        def get(self, address, password=None):
            s = sql.SQL('SELECT key_ciphertext FROM ethereum WHERE wallet_address_hex = %s')
            self.cur.execute(s, [ address ] )
            k = self.cur.fetchone()[0]
            return self._decrypt(k, password)


        def new(self, password=None):
            b = os.urandom(32)
            pk = keyapi.PrivateKey(b)

            pubk = keyapi.private_key_to_public_key(pk)
            address_hex = pubk.to_checksum_address()
            address_hex_clean = strip_hex_prefix(address_hex)

            logg.debug('address {}'.format(address_hex_clean))
            c = self._encrypt(pk.to_bytes(), password)
            s = sql.SQL('INSERT INTO ethereum (wallet_address_hex, key_ciphertext) VALUES (%s, %s)')
            self.cur.execute(s, [ address_hex_clean, c.decode('utf-8') ])
            self.conn.commit()
            return address_hex


        def _encrypt(self, private_key, password):
            f = self._generate_encryption_engine(password)
            return f.encrypt(private_key)


        def _generate_encryption_engine(self, password):
            h = sha3.keccak_256()
            h.update(self.symmetric_key)
            if password != None:
                password_bytes = to_bytes(password)
                h.update(password_bytes)
            g = h.digest()
            return Fernet(base64.b64encode(g))


        def _decrypt(self, c, password):
            f = self._generate_encryption_engine(password)
            return f.decrypt(c.encode('utf-8'))
             

        def __del__(self):
            logg.debug('closing database')
            self.conn.commit()
            self.cur.close()
            self.conn.close()
