# standard imports
import logging
import base64
import os

# third-party imports
from cryptography.fernet import Fernet
import psycopg2
from psycopg2 import sql
from eth_keys import KeyAPI
from eth_keys.backends import NativeECCBackend
import sha3

# local imports
from crypto_dev_signer.common import strip_hex_prefix
from .interface import Keystore

keyapi = KeyAPI(NativeECCBackend)

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger(__file__)


def to_bytes(x):
    return x.encode('utf-8')


class ReferenceKeystore(Keystore):

        schema = [
    """CREATE TABLE IF NOT EXISTS ethereum (
        id SERIAL NOT NULL PRIMARY KEY,
        key_ciphertext VARCHAR(256) NOT NULL,
        wallet_address_hex CHAR(40) NOT NULL
        );
""",
    """CREATE UNIQUE INDEX IF NOT EXISTS ethereum_address_idx ON ethereum ( wallet_address_hex );
""",
    ]

        def __init__(self, dbname, **kwargs):
            self.conn = psycopg2.connect('dbname=' + dbname)
            self.cur = self.conn.cursor()
            self.symmetric_key = kwargs.get('symmetric_key')


        def get(self, address, password=None):
            safe_address = strip_hex_prefix(address)
            s = sql.SQL('SELECT key_ciphertext FROM ethereum WHERE wallet_address_hex = %s')
            self.cur.execute(s, [ safe_address ] )
            k = self.cur.fetchone()[0]
            return self._decrypt(k, password)


        def new(self, password=None):
            b = os.urandom(32)
            pk = keyapi.PrivateKey(b)
            return self.import_key(pk, password)


        def import_key(self, pk, password=None):
            pubk = keyapi.private_key_to_public_key(pk)
            address_hex = pubk.to_checksum_address()
            address_hex_clean = strip_hex_prefix(address_hex)

            logg.debug('inserting address {}'.format(address_hex_clean))
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
