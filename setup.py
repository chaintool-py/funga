from setuptools import setup

f = open('README.md', 'r')
long_description = f.read()
f.close()

requirements = []
f = open('requirements.txt', 'r')
while True:
    l = f.readline()
    if l == '':
        break
    requirements.append(l.rstrip())
f.close()

sql_requirements = []
f = open('sql_requirements.txt', 'r')
while True:
    l = f.readline()
    if l == '':
        break
    sql_requirements.append(l.rstrip())
f.close()

test_requirements = []
f = open('test_requirements.txt', 'r')
while True:
    l = f.readline()
    if l == '':
        break
    test_requirements.append(l.rstrip())
f.close()

setup(
        name="funga",
        version="0.5.1a1",
        description="A signer and keystore daemon and library for cryptocurrency software development",
        author="Louis Holbrook",
        author_email="dev@holbrook.no",
        packages=[
            'funga.eth.signer',
            'funga.eth',
            'funga.cli',
            'funga.keystore',
            'funga.runnable',
            'funga',
            ],
        install_requires=requirements,
        extras_require={
            'sql': sql_requirements,
            },
        tests_require=test_requirements,
        long_description=long_description,
        long_description_content_type='text/markdown',
        entry_points = {
            'console_scripts': [
                'crypto-dev-daemon=funga.runnable.signer:main',
                'eth-keyfile=funga.runnable.keyfile:main',
                ],
            },
        url='https://gitlab.com/chaintool/funga',
        )
