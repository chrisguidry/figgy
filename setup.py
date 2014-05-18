#!/usr/bin/env python

from setuptools import setup, find_packages


version = '0.0.1'

setup(
    name="figgy",
    version=version,
    packages=find_packages(),
    zip_safe=False,
    description="figgy is sample code for interviews",
    long_description="""\
""",
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='',
    author_email='',
    dependency_links=[
    ],
    url='',
    license='BSD',
    include_package_data=True,
    install_requires=[
        'Django>=1.6',
        'lxml>=3.2.0',
        'django-nose>=1.2',
        'tox>=1.7',
        'mock>=1.0.1'
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
