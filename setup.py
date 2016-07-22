#!/usr/bin/env python3
from setuptools import setup


long_description = (open('README.rst').read() +
                    '\n\n' +
                    open('CHANGELOG.rst').read())


setup(
        name='flask_api_builder',
        version='0.1.0',
        description="A shortcut for stubbing out your Flask REST API's",
        long_description=long_description,
        author="Michael F Bryan",
        author_email='michaelfbryan@gmail.com',
        packages='flask_api_builder',
        include_package_data=True,
        license="MIT license",

        install_requires=[
            'jinja2',
            ],
        tests_require=[
            'pytest',
            'coverage',
            'pylint',
            ],
        test_suite='tests',

        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
        ],
)

