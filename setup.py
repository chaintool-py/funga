from setuptools import setup

setup(
        name="crypto-dev-signer",
        version="0.2.4",
        description="A signer and keystore daemon and library for cryptocurrency software development",
        author="Louis Holbrook",
        author_email="dev@holbrook.no",
        packages=[
            'crypto_dev_signer.eth.signer',
            'crypto_dev_signer.eth.web3ext',
            'crypto_dev_signer.eth',
            'crypto_dev_signer.keystore',
            'crypto_dev_signer',
            ],
        install_requires=[
            'web3',
            'psycopg2',
            'cryptography',
            'eth-keys',
            'pysha3',
            'rlp',
            'json-rpc',
            'confini==0.2.1',
            ], 
        scripts = [
            'scripts/crypto-dev-daemon',
            ],
        data_files = [('', ['LICENSE.txt'])],
        url='https://gitlab.com/nolash/crypto-dev-signer',
        )
