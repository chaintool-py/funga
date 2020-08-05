#!/usr/bin/python

import unittest
import logging

from rlp import encode as rlp_encode

from signer import ReferenceSigner
from transaction import Transaction

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


tx = {
    'from': "0xEB014f8c8B418Db6b45774c326A0E64C78914dC0",
    'gasPrice': "20000000000",
    'gas': "22000",
    'to': '0x3535353535353535353535353535353535353535',
    'value': "1000",
    'data': "deadbeef",
}

class TestSign(unittest.TestCase):

    pk = None
    nonce = -1


    def getPk(self, address):
        return self.pk


    def getNonce(self):
        self.nonce += 1
        return self.nonce


    def setUp(self):
        #self.pk = b'abcdefghijklmnopqrstuvwxyz012345' #random.sample(range(256), k=32)
        self.pk = bytes.fromhex('5087503f0a9cc35b38665955eb830c63f778453dd11b8fa5bd04bc41fd2cc6d6')


    def tearDown(self):
        logg.info('teardown empty')



    def test_serialize_transaction(self):
        t = Transaction(tx, 0)
        self.assertRegex(t.__class__.__name__, "Transaction")
        logg.debug('{}'.format(rlp_encode(t.serialize())))


    def test_sign_transaction(self):
        t = Transaction(tx, 461, 8995)
        s = ReferenceSigner(self.getPk)
        z = s.signTransaction(t)


if __name__ == '__main__':
    unittest.main()
