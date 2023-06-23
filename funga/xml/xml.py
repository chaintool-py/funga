# standard imports 
import os
from enum import Enum
import logging
import xml.etree.ElementTree as ET
from base64 import b64decode

# local imports
from funga.data import data_dir

logg = logging.getLogger(__name__)

SignatureAccept = Enum('SignatureAccept', 'CANONICALIZATION SIGNING TRANSFORM DIGEST')
SignatureVerify = Enum('SignatureVerify', 'SIGNATURE DIGEST PUBLICKEY')



def cryptobinary_to_int(v):
    b = b64decode(v)
    return int.from_bytes(b, byteorder='big')


class SignatureParser:

    namespaces = {
            '': "http://www.w3.org/2000/09/xmldsig#",
            'dsig11': "http://www.w3.org/2009/xmldsig11",
                  }

    def __init__(self, validate_schema=True):
        self.__tree = None
        self.__signature_verifier = None
        self.__settings = [
                [],
                [],
                [],
                [],
                ]
        self.__verify = [
                None,
                None,
                None,
                ]
        self.__schema = None
        if validate_schema:
            self.__load_schema_validator()
        self.clear()

    
    def __load_schema_validator(self):
        import importlib
        m = None
        try:
            m = importlib.import_module('xmlschema')
        except ModuleNotFoundError:
            return
        logg.info('found xmlschema module, will validate xml')
        #sp = os.path.join(data_dir, 'xmldsig1-schema.xsd')
        sp = os.path.join(data_dir, 'xmldsig-core-schema.xsd')
        self.__schema = m.XMLSchema(sp, validation='lax')
        # TODO: add validation for xmldsig11 OR make work with xmldsig1-schema bundle


    def clear(self):
        self.signature = None
        self.digest = None
        self.public_key = None
        self.prime = None
        self.curve_a = None
        self.curve_b = None
        self.base = None
        self.order = None
        self.cofactor = None
        self.keyname = None


    def set(self, k, v):
        if k.__class__.__name__ == 'SignatureAccept':
            self.__settings[k.value - 1].append(v)
        elif k.__class__.__name__ == 'SignatureVerify':
            self.__verify[k.value - 1] = v
        else:
            raise ValueError('invalid key: {}'.format(k))

    def get(self, k):
        if k.__class__.__name__ == 'SignatureAccept':
            return self.__settings[k.value - 1]
        elif k.__class__.__name__ == 'SignatureVerify':
            return self.__verify[k.value - 1]
        raise ValueError('invalid key: {}'.format(k))

    
    def __verify_schema(self, fp):
        if self.__schema == None:
            return
        self.__schema.validate(fp)


    def process_file(self, fp):
        self.__verify_schema(fp)
        self.__tree = ET.parse(fp)
        self.__root = self.__tree.getroot()
        self.__verify_canonicalization(self.__root[0][0])
        self.__verify_sign_method(self.__root[0][1])
        self.__verify_signature(self.__root[1])
        r = self.__root.find('./SignedInfo/Reference', namespaces=self.namespaces)
        if r != None:
            self.__opt_verify_signedinfo(r)
        r = self.__root.find('./KeyInfo', namespaces=self.namespaces)
        if r != None:
            self.__opt_verify_keyinfo(r)


    def __verify_canonicalization(self, el):
        assert el.attrib['Algorithm'] in self.get(SignatureAccept.CANONICALIZATION)


    def __verify_sign_method(self, el):
        assert el.attrib['Algorithm'] in self.get(SignatureAccept.SIGNING)


    def __verify_signature(self, el):
        b = b64decode(el.text)
        m = self.get(SignatureVerify.SIGNATURE)
        if m != None:
            assert m(b)
        self.signature = b

    def __opt_verify_signedinfo(self, el):
        r = el.find('./DigestMethod', namespaces=self.namespaces)
        if r != None:
            assert r.attrib['Algorithm'] in self.get(SignatureAccept.DIGEST)
        r = el.find('./DigestValue', namespaces=self.namespaces)
        if r != None:
            b = b64decode(r.text)
            m = self.get(SignatureVerify.DIGEST)
            if m != None:
                assert m(b)
            self.digest = b


    def __opt_verify_keyinfo(self, el):
        r = el.find('./dsig11:ECKeyValue', namespaces=self.namespaces)
        if r != None:
            self.__opt_verify_keyinfo_eckey(r)

        r = el.find('./KeyName', namespaces=self.namespaces)
        if r != None:
            self.keyname = r.text


    def __opt_verify_keyinfo_eckey(self, el):
        r = el.find('./dsig11:PublicKey', namespaces=self.namespaces)
        if r != None:
            b = b64decode(r.text)
            m = self.get(SignatureVerify.PUBLICKEY)
            if m != None:
                assert m(b)
            self.public_key = b
        r = el.find('./dsig11:ECParameters/dsig11:FieldID/dsig11:Prime/dsig11:P', namespaces=self.namespaces)
        self.prime = cryptobinary_to_int(r.text)
        r = el.find('./dsig11:ECParameters/dsig11:Curve/dsig11:A', namespaces=self.namespaces)
        self.curve_a = cryptobinary_to_int(r.text)
        r = el.find('./dsig11:ECParameters/dsig11:Curve/dsig11:B', namespaces=self.namespaces)
        self.curve_b = cryptobinary_to_int(r.text)
        r = el.find('./dsig11:ECParameters/dsig11:Base', namespaces=self.namespaces)
        self.base = cryptobinary_to_int(r.text)
        r = el.find('./dsig11:ECParameters/dsig11:Order', namespaces=self.namespaces)
        self.order = cryptobinary_to_int(r.text)
        r = el.find('./dsig11:ECParameters/dsig11:CoFactor', namespaces=self.namespaces)
        if r != None:
            self.cofactor = int(r.text)
