# standard imports
import os
import json
import logging

# local imports
from crypto_dev_signer.keystore import keyfile
from crypto_dev_signer.encoding import private_key_from_bytes

logg = logging.getLogger(__name__)

class Keystore:

    def get(self, address, password=None):
        raise NotImplementedError


    def list(self):
        raise NotImplementedError


    def new(self, password=None):
        b = os.urandom(32)
        return self.import_raw_key(b, password)


    def import_raw_key(self, b, password=None):
        pk = private_key_from_bytes(b)
        return self.import_key(pk, password)


    def import_key(self, pk, password=None):
        raise NotImplementedError


    def import_keystore_data(self, keystore_content, password=''):
        if type(keystore_content).__name__ == 'str':
            keystore_content = json.loads(keystore_content)
        elif type(keystore_content).__name__ == 'bytes':
            logg.debug('bytes {}'.format(keystore_content))
            keystore_content = json.loads(keystore_content.decode('utf-8'))
        private_key = keyfile.from_dict(keystore_content, password.encode('utf-8'))
        return self.import_raw_key(private_key, password)

    def import_keystore_file(self, keystore_file, password=''):
        private_key = keyfile.from_file(keystore_file, password)
        return self.import_raw_key(private_key)
