# standard imports
import logging
import unittest
import os
from base64 import b64decode

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
        self.parser.set(SignatureAccept.SIGNING, 'http://tools.ietf.org/html/rfc6931')

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

        self.assertEqual(self.parser.signature.hex(), 'af77767edbccdf46380fed6f06af43c807de4bedce2eda129923340e9577c97e76bc55d587103a367057167f351ae1cfd6b8dea6e0282257de3594fbe3d8780700')
        self.assertEqual(self.parser.public_key.hex(), '049f6bb6a7e3f5b7ee71756a891233d1415658f8712bac740282e083dc9240f5368bdb3b256a5bf40a8f7f9753414cb447ee3f796c5f30f7eb40a7f5018fc7f02e')
        self.assertEqual(self.parser.digest.hex(), '76b2e96714d3b5e6eb1d1c509265430b907b44f72b2a22b06fcd4d96372b8565')


if __name__ == '__main__':
    unittest.main()
