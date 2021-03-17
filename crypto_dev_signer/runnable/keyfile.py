# standard imports
import logging
import sys

# local imports
from crypto_dev_signer.keystore.keyfile import parse_file

print(from_file(sys.argv[1]).hex())
