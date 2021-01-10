# standard imports
import logging

# local imports
from crypto_dev_signer.helper import TxExecutor

logg = logging.getLogger()
logging.getLogger('web3').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


class EthTxExecutor(TxExecutor):

    def __init__(self, w3, sender, signer, chain_id, verifier=None, block=False):
        self.w3 = w3
        nonce = self.w3.eth.getTransactionCount(sender, 'pending')
        super(EthTxExecutor, self).__init__(sender, signer, self.translator, self.dispatcher, self.reporter, nonce, chain_id, self.fee_helper, self.fee_price_helper, verifier, block)


    def fee_helper(self, tx):
        estimate = self.w3.eth.estimateGas(tx)
        if estimate < 21000:
            estimate = 21000
        logg.debug('estimate {} {}'.format(tx, estimate))
        return estimate


    def fee_price_helper(self):
        return self.w3.eth.gasPrice


    def dispatcher(self, tx):
        return self.w3.eth.sendRawTransaction(tx)


    def reporter(self, tx):
        return self.w3.eth.getTransactionReceipt(tx)


    def translator(self, tx):
        if tx.get('feePrice') != None:
            tx['gasPrice'] = tx['feePrice']
            del tx['feePrice']

        if tx.get('feeUnits') != None:
            tx['gas'] = tx['feeUnits']
            del tx['feeUnits']

        return tx
