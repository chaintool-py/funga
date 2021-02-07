import uuid
import random
import json
import os
import logging
import time
import sha3
import sys
from urllib.request import Request, urlopen

from crypto_dev_signer.keystore import keyapi
from crypto_dev_signer.eth.transaction import EIP155Transaction
from crypto_dev_signer.eth.signer.defaultsigner import ReferenceSigner

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

pk_input = sys.argv[1]


class pkGetter:

    def __init__(self, pk):
        self.pk = pk

    def get(self, address, password=None):
        return self.pk


def init(pk_hex):
    pk_bytes = bytes.fromhex(pk_hex)
    pk = keyapi.PrivateKey(pk_bytes)

    pubk = keyapi.private_key_to_public_key(pk)
    address_hex = pubk.to_checksum_address()

    pk_getter = pkGetter(pk_bytes)
    
    signer = ReferenceSigner(pk_getter)

    return (signer, address_hex,)


def main():
    random.seed()

    (signer, address) = init(pk_input)

    req = Request('http://localhost:63545')
    req.add_header('Content-Type', 'application/json')
    o = {
        'jsonrpc': '2.0',
        'method': 'eth_getTransactionCount',
        'id': str(uuid.uuid4()),
        'params': [
            address,
            'pending',
            ],
            }
    res = urlopen(req, json.dumps(o).encode('utf-8'))
    o = json.loads(res.read().decode('utf-8'))
    hx = o['result'][2:]
    if len(hx) % 2 != 0:
        hx = '0' + hx
    nonce = int.from_bytes(bytes.fromhex(hx), 'big')
    logg.debug('using nonce {} for {}'.format(nonce, address))

    i = 0
    offset = nonce
    while True:
        gas_price = random.randint(1, 20) * 1000000000
        gas_limit = random.randint(21000, 8000000)
        to = '0x' + os.urandom(20).hex()
        value = random.randint(0, 2) * 100
        data = '0x'
        if value > 0:
            data += os.urandom(128).hex()

        tx = {
            'nonce': nonce,
            'from': "0xEB014f8c8B418Db6b45774c326A0E64C78914dC0",
            'gasPrice': gas_price,
            'gas': gas_limit,
            'to': to,
            'value': value,
            'data': data,
            'chainId': 8996,
        }
        
        txe = EIP155Transaction(tx, nonce, 8996)

        sign_and_send(signer, txe)

        nonce += 1
        i += 1

        logg.debug('tx {} ({}) ok'.format(nonce - offset + 1, nonce))

        if i == 100:
            logg.info('waiting a bit for node to catch up')
            time.sleep(7)
            i = 0


def sign_and_send(signer, txe, save=True):

        signer.signTransaction(txe)
        tx_raw = txe.rlp_serialize()
        
        h = sha3.keccak_256()
        h.update(tx_raw)
        tx_hash = h.digest().hex()

        if save:
            f = open(os.path.join('tmp', tx_hash), 'w')
            f.write(str(txe.serialize()) + '\n')
            f.write(tx_raw.hex())
            f.close()
        logg.info('sending tx {}'.format(tx_hash))

        req = Request('http://localhost:63545')
        req.add_header('Content-Type', 'application/json')
        o = {
            'jsonrpc': '2.0',
            'method': 'eth_sendRawTransaction',
            'id': str(uuid.uuid4()),
            'params': [
                '0x' + tx_raw.hex(),
                ],
                }
        res = urlopen(req, json.dumps(o).encode('utf-8'))
        o = json.loads(res.read().decode('utf-8'))
        logg.debug('response: {}'.format(o))
        if o.get('error') != None:
            logg.error('error: {}'.format(o.get('error')))
            sys.exit(1)


def redo():

        (signer, address) = init(pk_input)

        tx = {'nonce': 510, 'from': '0xEB014f8c8B418Db6b45774c326A0E64C78914dC0', 'gasPrice': 5000000000, 'gas': 6608539, 'to': '0x7fe37d3341b6044a3d9d84607b885db2a8ffda17', 'value': 100, 'data': '0xc2d9656585afddb615816c254fc99810e2b9bce6a27b7366f22c5e929960d7a8ce2d8a87d46826e6cee955d3594c772584712f6e11da929005b3b77bc0168f54ba6d38fbf3f9e9c5bf04abc799af46c34068998e14508135a3e9e6dda73bde0f306bf07c6e6558525f5d2744dc7c5ccc6161c2e7aad39214779a9dfb2ffdd466', 'chainId': 8996}

        txe = EIP155Transaction(tx, tx['nonce'], tx['chainId'])

        sign_and_send(signer, txe, save=False)
                

if __name__ == '__main__':
    main()
    #redo()
