from setuptools import setup

setup(
        name="crypto-dev-signer",
        version="0.1.0",
        description="A signer and keystore daemon and library for cryptocurrency software development",
        author="Louis Holbrook",
        author_email="dev@holbrook.no",
        packages=['crypto-dev-signer'],
        install_requires=['web3', 'psycopg2', 'cryptography', 'eth-keys', 'pysha3', 'rlp'], 
        scripts = [
            'scripts/crypto-dev-daemon.py',
            ],
        )
