import logging
import binascii

from rlp import encode as rlp_encode

from common import strip_hex_prefix

logg = logging.getLogger(__name__)

class Transaction:

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
        self.r = 0
        self.s = 0
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
            'nonce': '0x' + hex(self.nonce),
            'gasPrice': '0x' + hex(self.gas_price),
            'gas': '0x' + hex(self.start_gas),
            'to': '0x' + self.to.hex(),
            'value': '0x' + hex(self.value),
            'data': '0x' + self.data.hex(),
            'v': '0x' + hex(self.v),
            'r': '0x' + self.r.hex(),
            's': '0x' + self.s.hex(),
            }
