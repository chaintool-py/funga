# standard imports
import logging

# third-party imports
from crypto_dev_signer.eth.transaction import EIP155Transaction

# local imports
from crypto_dev_signer.error import TransactionRevertError

logg = logging.getLogger()


class TxExecutor:

    def __init__(self, sender, signer, dispatcher, reporter, nonce, chain_id, fee_helper, fee_price_helper, block=False):
        self.sender = sender
        self.nonce = nonce
        self.signer = signer
        self.dispatcher = dispatcher
        self.reporter = reporter
        self.block = bool(block)
        self.chain_id = chain_id
        self.tx_hashes = []
        self.fee_price_helper = fee_price_helper
        self.fee_helper = fee_helper


    def sign_and_send(self, builder, force_wait=False):
        fee_units = self.fee_helper(self.sender, None, None) 

        tx_tpl = {
            'from': self.sender,
            'chainId': self.chain_id,
            'fee': fee_units,
            'feePrice': self.fee_price_helper(),
            'nonce': self.nonce,
            }
        tx = None
        for b in builder:
            tx = b(tx_tpl, tx)

        logg.debug('from {} nonce {} tx {}'.format(self.sender, self.nonce, tx))

        chain_tx = EIP155Transaction(tx, self.nonce, self.chain_id)
        signature = self.signer.signTransaction(chain_tx)
        chain_tx_serialized = chain_tx.rlp_serialize()
        tx_hash = self.dispatcher('0x' + chain_tx_serialized.hex())
        self.tx_hashes.append(tx_hash)
        self.nonce += 1
        rcpt = None
        if self.block or force_wait:
            rcpt = self.wait_for(tx_hash)
            logg.info('tx {} fee used: {}'.format(tx_hash.hex(), rcpt['feeUsed']))
        return (tx_hash.hex(), rcpt)


    def wait_for(self, tx_hash=None):
        if tx_hash == None:
            tx_hash = self.tx_hashes[len(self.tx_hashes)-1]
        i = 1
        while True:
            try:
                #return self.w3.eth.getTransactionReceipt(tx_hash)
                return self.reporter(tx_hash)
            except web3.exceptions.TransactionNotFound:
                logg.debug('poll #{} for {}'.format(i, tx_hash.hex()))   
                i += 1
                time.sleep(1)
        if rcpt['status'] == 0:
            raise TransactionRevertError(tx_hash)
        return rcpt
