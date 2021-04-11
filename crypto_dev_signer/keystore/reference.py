# standard imports
import logging
import base64

# external imports
from cryptography.fernet import Fernet
#import psycopg2
#from psycopg2 import sql
#from psycopg2.extensions import make_dsn
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sha3
from hexathon import (
        strip_0x,
        add_0x,
        )

# local imports
from .interface import Keystore
#from . import keyapi
from crypto_dev_signer.error import UnknownAccountError
from crypto_dev_signer.encoding import private_key_to_address

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

        def __init__(self, dsn, **kwargs):
            logg.debug('starting db session with dsn {}'.format(dsn))
            self.db_engine = create_engine(dsn)
            self.db_session = sessionmaker(bind=self.db_engine)()
            for s in self.schema:
                self.db_session.execute(s)
                self.db_session.commit()
            self.symmetric_key = kwargs.get('symmetric_key')


        def __del__(self):
            logg.debug('closing db session')
            self.db_session.close()


        def get(self, address, password=None):
            safe_address = strip_0x(address).lower()
            s = text('SELECT key_ciphertext FROM ethereum WHERE wallet_address_hex = :a')
            r = self.db_session.execute(s, {
                'a': safe_address,
                },
                )
            try:
                k = r.first()[0]
            except TypeError:
                self.db_session.rollback()
                raise UnknownAccountError(safe_address)
            self.db_session.commit()
            a = self._decrypt(k, password)
            return a


        def import_key(self, pk, password=None):
            address_hex = private_key_to_address(pk)
            address_hex_clean = strip_0x(address_hex).lower()

            c = self._encrypt(pk.secret, password)
            s = text('INSERT INTO ethereum (wallet_address_hex, key_ciphertext) VALUES (:a, :c)') #%s, %s)')
            self.db_session.execute(s, {
                'a': address_hex_clean,
                'c': c.decode('utf-8'),
                },
                )
            self.db_session.commit()
            logg.info('added private key for address {}'.format(address_hex_clean))
            return add_0x(address_hex)


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