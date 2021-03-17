# standard imports
import os
import logging
import sys
import json
import argparse
import getpass

# external impors
import coincurve

# local imports
from crypto_dev_signer.keystore.keyfile import (
        from_file,
        to_dict,
        )


logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

argparser = argparse.ArgumentParser()
argparser.add_argument('-d', type=str, help='decrypt file')
argparser.add_argument('-v', action='store_true', help='be verbose')
args = argparser.parse_args()

if args.v:
    logg.setLevel(logging.DEBUG)

mode = 'create'
if args.d:
    mode = 'decrypt'

def main():
    passphrase = os.environ.get('PASSPHRASE')
    r = None
    if mode == 'decrypt':
        if passphrase == None:
            passphrase = getpass.getpass('decryption phrase: ')
        try:
            r = from_file(args.d, passphrase).hex()
        except AssertionError:
            sys.stderr.write('Invalid passphrase\n')
            sys.exit(1)
    elif mode == 'create':
        if passphrase == None:
            passphrase = getpass.getpass('encryption phrase: ')
        pk_bytes = os.urandom(32)
        pk = coincurve.PrivateKey(secret=pk_bytes)
        o = to_dict(pk, passphrase)
        r = json.dumps(o)

    print(r) 


if __name__ == '__main__':
    main()
