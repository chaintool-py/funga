import logging
import base64
import os

from cryptography.fernet import Fernet
import psycopg2
from psycopg2 import sql
from eth_keys import KeyAPI
from eth_keys.backends import NativeECCBackend
import sha3

keyapi = KeyAPI(NativeECCBackend)

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger(__file__)



def to_bytes(x):
    return x.encode('utf-8')

    
class ReferenceDatabase:


        def __init__(self, dbname, **kwargs):
            logg.debug(kwargs)
            self.conn = psycopg2.connect('dbname='+dbname)
            self.cur = self.conn.cursor()
            self.symmetric_key = kwargs.get('symmetric_key')


        def get(self, address, password=None):
            s = sql.SQL('SELECT key_ciphertext FROM ethereum WHERE wallet_address_hex = %s')
            logg.debug(address)
            self.cur.execute(s, [ address ] )
            k = self.cur.fetchone()[0]
            return self._decrypt(k, password)


        def new(self, address, password=None):
            b = os.urandom(32)
            pk = keyapi.PrivateKey(b)
            logg.debug('pk {}'.format(pk.to_hex()))
            c = self._encrypt(pk.to_bytes(), password)
            logg.debug('pkc {} {}'.format(c, len(pk.to_bytes())))
            s = sql.SQL('INSERT INTO ethereum (wallet_address_hex, key_ciphertext) VALUES (%s, %s)')
            self.cur.execute(s, [ address, c.decode('utf-8') ])


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
             

        def __exit__(self):
            self.conn
            self.cur.close()
            self.conn.close()
