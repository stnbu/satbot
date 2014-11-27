# -*- coding: utf-8 -*-

from setuptools import setup

import satbot

NAME = 'satbot'

# README.rst dynamically generated:
with open('README.rst', 'w') as f:
    f.write(satbot.__doc__)


def read(file):
    with open(file, 'r') as f:
        return f.read().strip()

setup(
    name=NAME,
    version=read('VERSION'),
    description='Read data from commonly-available "satellite" hobby R/C receivers.',
    long_description=read('README.rst'),
    author='Mike Burr',
    author_email='mburr@unintuitive.org',
    url='https://github.com/stnbu/{0}'.format(NAME),
    download_url='https://github.com/stnbu/{0}/archive/master.zip'.format(NAME),
    license='MIT',
    provides=[NAME],
    bugtrack_url='https://github.com/stnbu/{0}/issues'.format(NAME),
    requires=['daemon', 'pyserial'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Topic :: Games/Entertainment',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: System :: Hardware',
        'Topic :: Terminals :: Serial',
    ],
    packages=[NAME],
    keywords=['r/c', 'robotics', 'dsm'],
    test_suite='nose.collector',
    test_requires=['nose', 'runpy'],
    entry_points={
        'console_scripts': [
            'satbot = satbot.run:run',
        ],
        'gui_script': []},
)
