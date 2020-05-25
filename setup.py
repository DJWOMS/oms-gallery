# /usr/bin/env python
import os

from setuptools import setup

import oms_gallery


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


with open('requirements.txt') as f:
    reqs = f.read().splitlines()


setup(
    name="oms_gallery",
    version=oms_gallery.__version__,
    description="Image management for Django.",
    author="Omelchenko Michael - DJWOMS",
    author_email="djwoms@gmail.com",
    url="https://github.com/DJWOMS/oms-gallery",
    long_description=read('README.md'),
    packages=['oms_gallery'],
    include_package_data=True,
    zip_safe=False,
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Topic :: Utilities'],
    install_requires=reqs,
)
