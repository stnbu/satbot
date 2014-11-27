# -*- coding: utf-8 -*-

from setuptools import setup

import satbot

# README.rst dynamically generated:
with open('README.rst', 'w') as f:
    f.write(satbot.__doc__)


def read(file):
    with open(file, 'r') as f:
        return f.read().strip()

setup(
    name='satbot',
    version=read('VERSION'),
    description='Read data from commonly-available "satellite" hobby R/C receivers.',
    long_description=read('README.rst'),
    author='Mike Burr',
    author_email='mburr@unintuitive.org',
    url='https://github.com/stnbu/satbot',
    download_url='https://github.com/stnbu/satbot/archive/master.zip',
    license='MIT',
    #classifiers=[
    #    'Development Status :: 4 - Beta',
    #    'Intended Audience :: Developers',
    #    'License :: OSI Approved :: MIT License',
    #    'Programming Language :: Python :: 2',
    #    'Topic :: Software Development',
    #    'Topic :: Utilities',
    #],
    packages=['satbot'],
    #keywords=['configuration', 'registry', 'refactor'],
    #test_suite='nose.collector',
    #test_requires=['nose'],
    entry_points={
        'console_scripts': [
            'satbot = satbot.run:run',
        ],
        'gui_script': []},
)
