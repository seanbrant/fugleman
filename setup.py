import codecs
import os
from setuptools import find_packages, setup

import fugleman


def read(*paths):
    with codecs.open(os.path.join(os.path.dirname(__file__), *paths)) as f:
        return f.read()


setup(
    name='Fugleman',
    version=fugleman.__version__,
    description='A simple WSGI app that makes it easy to serve web prototypes.',
    long_description=read('README.rst'),
    author='Sean Brant',
    author_email='brant.sean@gmail.com',
    license='BSD',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fug = fugleman.cli:run',
        ]
    },
)
