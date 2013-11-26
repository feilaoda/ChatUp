#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='feilaoda',
    version='1.0.0',
    author='feilaoda',
    author_email='feilaoda@me.com',
    url='http://feilaoda.me',
    packages=find_packages(),
    description='',
    install_requires=[
        'tornado==2.4', 
        'dojang==1.0',    
        'pygments',
        'sqlalchemy==2.7',
        'MySQL-python',
        'python-memcached',
        'PIL',
    ],
    include_package_data=True,
)
