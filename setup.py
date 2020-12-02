from setuptools import setup

f = open('README.md', 'r')
long_description = f.read()
f.close()

setup(
        name="crypto-dev-signer",
        version="0.4.1",
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
            'web3==5.12.2',
            'psycopg2==2.8.6',
            'cryptography==3.2.1',
            'eth-keys==0.3.3',
            'pysha3==1.0.2',
            'rlp==1.2.0',
            'json-rpc==1.13.0',
            'confini==0.3.2',
            'sqlalchemy==1.3.20',
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
