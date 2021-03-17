# standard imports
import os
import logging
import sys
import json
import argparse

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
argparser.add_argument('arg', type=str, help='decrypt file')
args = argparser.parse_args()

if args.v:
    logg.setLevel(logging.DEBUG)

r = None
if args.d:
    try:
        r = from_file(args.d, args.arg).hex()
    except AssertionError:
        sys.stderr.write('Invalid passphrase\n')
        sys.exit(1)
else:
    pk_bytes = os.urandom(32)
    pk = coincurve.PrivateKey(secret=pk_bytes)
    o = to_dict(pk, args.arg)
    r = json.dumps(o)

print(r) 
