# standard imports 
from enum import Enum
import logging
import xml.etree.ElementTree as ET
from base64 import b64decode

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

    def __init__(self):
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
        self.__r = None
        self.clear()


    def clear(self):
        self.__r = {
                'sig': None,
                'pubkey': None,
                'prime': None,
                'curve_a': None,
                'curve_b': None,
                'base': None,
                'order': None,
                'cofactor': None,
                'keyname': None,
                }


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


    def process_file(self, fp):
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
        logg.debug('result {}'.format(self.__r))


    def __verify_canonicalization(self, el):
        assert el.attrib['Algorithm'] in self.get(SignatureAccept.CANONICALIZATION)


    def __verify_sign_method(self, el):
        assert el.attrib['Algorithm'] in self.get(SignatureAccept.SIGNING)


    def __verify_signature(self, el):
        b = b64decode(el.text)
        m = self.get(SignatureVerify.SIGNATURE)
        if m != None:
            assert m(b)
        self.__r['sig'] = b

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
            self.__r['digest'] = b


    def __opt_verify_keyinfo(self, el):
        r = el.find('./dsig11:ECKeyValue', namespaces=self.namespaces)
        if r != None:
            assert self.__opt_verify_keyinfo_eckey(r)

        r = el.find('./KeyName', namespaces=self.namespaces)
        if r != None:
            self.__r['keyname'] = r.text


    def __opt_verify_keyinfo_eckey(self, el):
        r = el.find('./dsig11:PublicKey', namespaces=self.namespaces)
        if r != None:
            b = b64decode(r.text)
            m = self.get(SignatureVerify.PUBLICKEY)
            if m != None:
                assert m(b)
            self.__r['pubkey'] = b
        r = el.find('./dsig11:ECParameters/dsig11:FieldID/dsig11:Prime/dsig11:P', namespaces=self.namespaces)
        self.__r['prime'] = cryptobinary_to_int(r.text)
        r = el.find('./dsig11:ECParameters/dsig11:Curve/dsig11:A', namespaces=self.namespaces)
        self.__r['curve_a'] = cryptobinary_to_int(r.text)
        r = el.find('./dsig11:ECParameters/dsig11:Curve/dsig11:B', namespaces=self.namespaces)
        self.__r['curve_b'] = cryptobinary_to_int(r.text)
        r = el.find('./dsig11:ECParameters/dsig11:Base', namespaces=self.namespaces)
        self.__r['base'] = cryptobinary_to_int(r.text)
        r = el.find('./dsig11:ECParameters/dsig11:Order', namespaces=self.namespaces)
        self.__r['order'] = cryptobinary_to_int(r.text)
        r = el.find('./dsig11:ECParameters/dsig11:CoFactor', namespaces=self.namespaces)
        self.__r['cofactor'] = int(r.text)

        return True
