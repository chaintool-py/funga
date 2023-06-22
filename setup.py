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

test_requirements = []
f = open('test_requirements.txt', 'r')
while True:
    l = f.readline()
    if l == '':
        break
    test_requirements.append(l.rstrip())
f.close()

xml_requirements = []
f = open('xml_requirements.txt', 'r')
while True:
    l = f.readline()
    if l == '':
        break
    xml_requirements.append(l.rstrip())
f.close()

setup(
        name="funga",
        version="0.5.7",
        description="A signer and keystore daemon and library for cryptocurrency software development",
        author="Louis Holbrook",
        author_email="dev@holbrook.no",
        packages=[
            'funga',
            ],
        install_requires=requirements,
        tests_require=test_requirements,
        long_description=long_description,
        long_description_content_type='text/markdown',
        extras_require={
            'xml': xml_requirements,
            },
        url='https://git.defalsify.org/funga',
        )
