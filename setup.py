# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='APC',
    version='2.0',
    long_description=__doc__,
    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Login',
        'Flask-WTF',
    ]
)
