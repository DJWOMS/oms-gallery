# /usr/bin/env python
from setuptools import setup, find_packages
from pkg_resources import parse_requirements

import oms_gallery


def get_requirements(source):
    with open(source) as f:
        return sorted({str(req) for req in parse_requirements(f.read())})


setup(
    name="oms-gallery",
    version=oms_gallery.__version__,
    description="Image management for Django.",
    author="Omelchenko Michael - DJWOMS",
    author_email="djwoms@gmail.com",
    url="https://github.com/DJWOMS/",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=['Development Status :: 1 - Beta',
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
    install_requires=get_requirements('requirements.txt'),
)
