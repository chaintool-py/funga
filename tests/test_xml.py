# standard imports
import logging
import unittest
import os
from base64 import b64decode
from hashlib import sha256

# external imports
from fastecdsa import curve
from fastecdsa import ecdsa

# local imports
from funga.xml import SignatureParser
from funga.xml import SignatureAccept
from funga.xml import SignatureVerify

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

test_dir = os.path.dirname(os.path.realpath(__file__))


def verify_fail(v):
    return False


def verify_sig_ok(v):
    return len(v) == 65

verify_pub_ok = verify_sig_ok

def verify_digest_ok(v):
    return len(v) == 32


class TestXmlSig(unittest.TestCase):

    def setUp(self):
        self.xml_file = os.path.join(test_dir, 'testdata', 'sign.xml')
        self.parser = SignatureParser()


    def test_base(self):
        with self.assertRaises(AssertionError):
            self.parser.process_file(self.xml_file)
        self.parser.set(SignatureAccept.CANONICALIZATION, 'http://www.w3.org/TR/2001/REC-xml-c14n-20010315')

        with self.assertRaises(AssertionError):
            self.parser.process_file(self.xml_file)
        self.parser.set(SignatureAccept.SIGNING, 'http://www.w3.org/2001/04/xmldsig-more#ecdsa-sha256')

        with self.assertRaises(AssertionError):
            self.parser.process_file(self.xml_file)
        self.parser.set(SignatureAccept.DIGEST, 'https://csrc.nist.gov/glossary/term/sha_256')
        self.parser.process_file(self.xml_file)
        
        self.parser.set(SignatureVerify.SIGNATURE, verify_fail)
        with self.assertRaises(AssertionError):
            self.parser.process_file(self.xml_file)
        self.parser.set(SignatureVerify.SIGNATURE, verify_sig_ok)
        self.parser.process_file(self.xml_file)

        self.parser.set(SignatureVerify.DIGEST, verify_fail)
        with self.assertRaises(AssertionError):
            self.parser.process_file(self.xml_file)
        self.parser.set(SignatureVerify.DIGEST, verify_sig_ok)
        with self.assertRaises(AssertionError):
            self.parser.process_file(self.xml_file)
        self.parser.set(SignatureVerify.DIGEST, verify_digest_ok)
        self.parser.process_file(self.xml_file)

        self.parser.set(SignatureVerify.PUBLICKEY, verify_fail)
        with self.assertRaises(AssertionError):
            self.parser.process_file(self.xml_file)
        self.parser.set(SignatureVerify.PUBLICKEY, verify_digest_ok)
        with self.assertRaises(AssertionError):
            self.parser.process_file(self.xml_file)
        self.parser.set(SignatureVerify.PUBLICKEY, verify_pub_ok)
        self.parser.process_file(self.xml_file)

        self.assertEqual(self.parser.sig_r, 88049138661219786673382328446851442949676708152514327418479271802005342599993)
        self.assertEqual(self.parser.sig_s, 15014121175306622951266769875074899597152611817081922798245423703943058669330)
        self.assertEqual(self.parser.public_key.hex(), '049f6bb6a7e3f5b7ee71756a891233d1415658f8712bac740282e083dc9240f5368bdb3b256a5bf40a8f7f9753414cb447ee3f796c5f30f7eb40a7f5018fc7f02e')
        self.assertEqual(self.parser.digest.hex(), 'e08f5c88dd7b076fe3e42f9146980a3c8223324ef7aa3b5b9a6103a6ca657b42')

        h = sha256()
        h.update(self.parser.sign_material.encode('utf-8'))
        digest_outer = h.digest()
        self.assertEqual(digest_outer.hex(), 'c34e546b70afeb6962d6faa59eb7f9316fc254cc96534cd181aff6958004c5ee')

        c = curve.Curve(
                'eth',
                self.parser.prime,
                self.parser.curve_a,
                self.parser.curve_b,
                self.parser.order,
                self.parser.base_x,
                self.parser.base_y,
                )

        class Pubk:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        x = int.from_bytes(self.parser.public_key[1:33], byteorder='big')
        y = int.from_bytes(self.parser.public_key[33:65], byteorder='big')
        pubk = Pubk(x, y)

        r = ecdsa.verify(
                (self.parser.sig_r, self.parser.sig_s),
                self.parser.sign_material,
                pubk,
                curve=c,
                hashfunc=sha256,
                )
        self.assertTrue(r)


if __name__ == '__main__':
    unittest.main()
