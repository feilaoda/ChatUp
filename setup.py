#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='feilaoda',
    version='1.0.0',
    author='feilaoda',
    author_email='feilaoda@me.com',
    url='http://www.wecoders.com',
    packages=find_packages(),
    description='',
    install_requires=[
        'tornado==3.2',
        'dojang==1.0',
        'pygments',
        'sqlalchemy==0.8.6',
        'MySQL-python',
        'python-memcached',
        'PIL',
        'formencode',
    ],
    include_package_data=True,
)
