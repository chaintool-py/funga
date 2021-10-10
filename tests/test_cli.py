# standard imports
import unittest
import logging
import os

# external imports
from hexathon import strip_0x

# local imports
from funga.eth.signer import EIP155Signer
from funga.eth.keystore.dict import DictKeystore
from funga.eth.cli.handle import SignRequestHandler
from funga.eth.transaction import EIP155Transaction

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(script_dir, 'testdata')

class TestCli(unittest.TestCase):

    def setUp(self):
        #pk = bytes.fromhex('5087503f0a9cc35b38665955eb830c63f778453dd11b8fa5bd04bc41fd2cc6d6')
        #pk_getter = pkGetter(pk)
        self.keystore = DictKeystore()
        SignRequestHandler.keystore = self.keystore
        self.signer = EIP155Signer(self.keystore)
        SignRequestHandler.signer = self.signer
        self.handler = SignRequestHandler()


    def test_new_account(self):
        q = {
                'id': 0,
                'method': 'personal_newAccount',
                'params': [''],
                }
        (rpc_id, result) = self.handler.process_input(q)
        self.assertTrue(self.keystore.get(result))


    def test_sign_tx(self):
        keystore_file = os.path.join(data_dir, 'UTC--2021-01-08T18-37-01.187235289Z--00a329c0648769a73afac7f9381e08fb43dbea72')
        sender = self.keystore.import_keystore_file(keystore_file)
        tx_hexs = {
            'nonce': '0x',
            'from': sender,
            'gasPrice': "0x04a817c800",
            'gas': "0x5208",
            'to': '0x3535353535353535353535353535353535353535',
            'value': "0x03e8",
            'data': "0xdeadbeef",
            'chainId': 8995,
        }
        tx = EIP155Transaction(tx_hexs, 42, 8995)
        tx_s = tx.serialize()

        # TODO: move to serialization wrapper for tests
        tx_s['chainId'] = tx_s['v']
        tx_s['from'] = sender

        # eth_signTransaction wraps personal_signTransaction, so here we test both already
        q = {
                'id': 0,
                'method': 'eth_signTransaction',
                'params': [tx_s],
                }
        (rpc_id, result) = self.handler.process_input(q)
        logg.debug('result {}'.format(result))

        self.assertEqual(strip_0x(result), 'f86c2a8504a817c8008252089435353535353535353535353535353535353535358203e884deadbeef82466aa0b7c1bbf52f736ada30fe253c7484176f44d6fd097a9720dc85ae5bbc7f060e54a07afee2563b0cf6d00333df51cc62b0d13c63108b2bce54ce2ad24e26ce7b4f25')

    def test_sign_msg(self):
        keystore_file = os.path.join(data_dir, 'UTC--2021-01-08T18-37-01.187235289Z--00a329c0648769a73afac7f9381e08fb43dbea72')
        sender = self.keystore.import_keystore_file(keystore_file)
        q = {
                'id': 0,
                'method': 'eth_sign',
                'params': [sender, '0xdeadbeef'],
                }
        (rpc_id, result) = self.handler.process_input(q)
        logg.debug('result msg {}'.format(result))
        self.assertEqual(strip_0x(result), '50320dda75190a121b7b5979de66edadafd02bdfbe4f6d49552e79c01410d2464aae35e385c0e5b61663ff7b44ef65fa0ac7ad8a57472cf405db399b9dba3e1600')


if __name__ == '__main__':
    unittest.main()
