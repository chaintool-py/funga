# standard imports
import os
import sys
import logging 
import argparse

# third-party imports
import confini

# local imports
from crypto_dev_signer.keystore import ReferenceKeystore

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

config_dir = os.path.join('/usr/local/etc/cic-eth')

db = None


argparser = argparse.ArgumentParser()
argparser.add_argument('-c', type=str, default=config_dir, help='config file')
argparser.add_argument('--env-prefix', default=os.environ.get('CONFINI_ENV_PREFIX'), dest='env_prefix', type=str, help='environment prefix for variables to overwrite configuration')
argparser.add_argument('-v', action='store_true', help='be verbose')
argparser.add_argument('-vv', action='store_true', help='be more verbose')
argparser.add_argument('private_key', type=str, help='private key to add, 0x hex format')
args = argparser.parse_args()

if args.vv:
    logging.getLogger().setLevel(logging.DEBUG)
elif args.v:
    logging.getLogger().setLevel(logging.INFO)

config = confini.Config(args.c, args.env_prefix)
config.process()
config.censor('PASSWORD', 'DATABASE')
config.censor('SECRET', 'SIGNER')
logg.debug('config loaded from {}:\n{}'.format(config_dir, config))

# connect to database
dsn = 'postgresql://{}:{}@{}:{}/{}'.format(
        config.get('DATABASE_USER'),
        config.get('DATABASE_PASSWORD'),
        config.get('DATABASE_HOST'),
        config.get('DATABASE_PORT'),
        config.get('DATABASE_NAME'),    
    )

logg.info('using dsn {}'.format(dsn))


if __name__ == '__main__':
    kw = {
        'symmetric_key': bytes.fromhex(config.get('SIGNER_SECRET')),
        }
    r = ReferenceKeystore(dsn, **kw)
    private_key_bytes = bytes.fromhex(args.private_key)
    r.import_raw_key(private_key_bytes)
