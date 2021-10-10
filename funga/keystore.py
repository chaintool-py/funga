# standard imports
import os
import json
import logging

logg = logging.getLogger(__name__)


class Keystore:


    def __init__(self, private_key_generator, private_key_parser, keystore_parser):
        self.private_key_generator = private_key_generator
        self.private_key_parser = private_key_parser
        self.keystore_parser = keystore_parser


    def get(self, address, password=None):
        raise NotImplementedError


    def list(self):
        raise NotImplementedError


    def lock(self, address=None):
        raise NotImplementedError
       

    def unlock(self, address=None):
        raise NotImplementedError


    def new(self, password=None):
        self.private_key_generator(password=password)
       

    def import_raw_key(self, b, password=None):
        pk = self.private_key_parser(b)
        return self.import_key(pk, password)


    def import_key(self, pk, password=None):
        raise NotImplementedError


    def import_keystore_data(self, keystore_content, password=''):
        private_key = self.keystore_parser(keystore_content, password.encode('utf-8'))
        return self.import_raw_key(private_key, password=password)


    def import_keystore_file(self, keystore_file, password=''):
        private_key = self.keystore_parser(keystore_file, password)
        return self.import_raw_key(private_key, password=password)
