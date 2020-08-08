# standard imports
import logging
import binascii

# third-party imports
from rlp import encode as rlp_encode

# local imports
from crypto_dev_signer.common import strip_hex_prefix, add_hex_prefix

logg = logging.getLogger(__name__)


class Transaction:
    
    def rlp_serialize(self):
        raise NotImplementedError

    def serialize(self):
        raise NotImplementedError


class EIP155Transaction:

    def __init__(self, tx, nonce, chainId=1):
       
        to = binascii.unhexlify(strip_hex_prefix(tx['to']))
        data = binascii.unhexlify(strip_hex_prefix(tx['data']))

        self.nonce = nonce
        self.gas_price = int(tx['gasPrice'])
        self.start_gas = int(tx['gas'])
        self.to = to
        self.value = int(tx['value'])
        self.data = data
        self.v = chainId
        self.r = b''
        self.s = b''
        self.sender = strip_hex_prefix(tx['from'])


    def rlp_serialize(self):
        b = self.nonce.to_bytes(8, byteorder='little')
        s = [
            self.nonce,
            self.gas_price,
            self.start_gas,
            self.to,
            self.value,
            self.data,
            self.v,
            self.r,
            self.s,
                ]
        return rlp_encode(s)

    def serialize(self):
        return {
            'nonce': add_hex_prefix(hex(self.nonce)),
            'gasPrice': add_hex_prefix(hex(self.gas_price)),
            'gas': add_hex_prefix(hex(self.start_gas)),
            'to': add_hex_prefix(self.to.hex()),
            'value': add_hex_prefix(hex(self.value)),
            'data': add_hex_prefix(self.data.hex()),
            'v': add_hex_prefix(hex(self.v)),
            'r': add_hex_prefix(self.r.hex()),
            's': add_hex_prefix(self.s.hex()),
            }