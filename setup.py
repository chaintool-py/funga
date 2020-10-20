from setuptools import setup

f = open('README.md', 'r')
long_description = f.read()
f.close()

setup(
        name="crypto-dev-signer",
        version="0.3.0",
        description="A signer and keystore daemon and library for cryptocurrency software development",
        author="Louis Holbrook",
        author_email="dev@holbrook.no",
        packages=[
            'crypto_dev_signer.eth.signer',
            'crypto_dev_signer.eth.web3ext',
            'crypto_dev_signer.eth',
            'crypto_dev_signer.keystore',
            'crypto_dev_signer.runnable',
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
            'confini==0.2.6',
            'sqlalchemy==1.3.19',
            ], 
        long_description=long_description,
        long_description_content_type='text/markdown',
        #scripts = [
        #    'scripts/crypto-dev-daemon',
        #    ],
        entry_points = {
            'console_scripts': [
                'crypto-dev-daemon=crypto_dev_signer.runnable.signer:main',
                ],
            },
        url='https://gitlab.com/nolash/crypto-dev-signer',
        )
