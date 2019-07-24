# /usr/bin/env python
import os

from setuptools import setup, find_packages

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

import oms_gallery


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


install_reqs = parse_requirements('requirements.txt', session='hack')
reqs = [str(ir.req) for ir in install_reqs]


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
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Topic :: Utilities'],
    install_requires=reqs,
)
