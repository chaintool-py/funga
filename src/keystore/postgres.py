import logging
import base64

from cryptography.fernet import Fernet
import psycopg2
from psycopg2 import sql

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger(__file__)


class ReferenceDatabase:


        def __init__(self, dbname, **kwargs):
            logg.debug(kwargs)
            self.conn = psycopg2.connect('dbname='+dbname)
            self.cur = self.conn.cursor()
            self.cryptengine = None
            if kwargs.get('symmetric_key') != None:
                be = kwargs.get('symmetric_key')
                self.cryptengine = Fernet(base64.b64encode(be))


        def get(self, address):
            s = sql.SQL('SELECT key_ciphertext FROM ethereum WHERE wallet_address_hex = %s')
            logg.debug(address)
            self.cur.execute(s, [ address ] )
            k = self.cur.fetchone()[0]
            return self.decrypt(k)


        def decrypt(self, c):
            if self.cryptengine == None:
                return c
            logg.debug('decryption')
            return self.cryptengine.decrypt(c.encode('utf-8'))
             

        def __exit__(self):
            self.conn
            self.cur.close()
            self.conn.close()
