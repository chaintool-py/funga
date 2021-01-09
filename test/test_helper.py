# standard imports
import unittest
import logging
import os

# local imports
from crypto_dev_signer.keystore import DictKeystore
from crypto_dev_signer.eth.signer import ReferenceSigner
from crypto_dev_signer.helper import TxExecutor

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

script_dir = os.path.realpath(os.path.dirname(__file__))


class MockEthTxBackend:

    def dispatcher(self, tx):
        logg.debug('sender {}'.format(tx))
        return os.urandom(32)

    def reporter(self, tx):
        logg.debug('reporter {}'.format(tx))

    def verifier(self, rcpt):
        logg.debug('reporter {}'.format(rcpt))

    def fee_price_helper(self):
        return 21

    def fee_helper(self, sender, code, inputs):
        logg.debug('fee helper code {} inputs {}'.format(code, inputs))
        return 2

    def builder(self, tx):
        return {
            'from': tx['from'],
            'to': '0x' + os.urandom(20).hex(),
            'data': '',
            'gasPrice': tx['feePrice'],
            'gas': tx['feeUnits'],
            }
        
    def builder_two(self, tx):
        tx['value'] = 1024
        return tx


class TestHelper(unittest.TestCase):

    def setUp(self):
        logg.debug('setup')
        self.db = DictKeystore()
        
        keystore_filename = 'UTC--2021-01-08T18-37-01.187235289Z--00a329c0648769a73afac7f9381e08fb43dbea72'
        keystore_filepath = os.path.join(script_dir, 'testdata', keystore_filename)

        self.address_hex = self.db.import_keystore_file(keystore_filepath, '')
        self.signer = ReferenceSigner(self.db)


    def tearDown(self):
        pass


    def test_helper(self):
        backend = MockEthTxBackend()
        executor = TxExecutor(self.address_hex, self.signer, backend.dispatcher, backend.reporter, 666, 13, backend.fee_helper, backend.fee_price_helper, backend.verifier)    

        tx_ish = {'from': self.address_hex}
        executor.sign_and_send([backend.builder, backend.builder_two])


if __name__ == '__main__':
    unittest.main()
