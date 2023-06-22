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


if __name__ == '__main__':
    unittest.main()
