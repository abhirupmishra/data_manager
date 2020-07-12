#!/usr/bin/env python
from setuptools import setup, find_packages
import versioneer
import sys

long_description = ''

if 'upload' in sys.argv:
    with open('README.md') as f:
        long_description = f.read()

install_reqs = [
    'pandas >= 1.0.5',
    'sqlalchemy >= 1.3.18',
    'psycopg2 >= 2.8.5',
    'sqlacodegen >= 2.2.0'
]

extra_reqs = {
    'test': [
        "nose>=1.3.7",
        "parameterized>=0.5.0",
        "tox>=2.3.1",
        "flake8>=3.7.9",
    ],
}

if __name__ == "__main__":
    setup(
        name='data_manager',
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        description='Database utils for Postgres SQL',
        author='Abhirup Mishra',
        author_email='abhirupmishra@gmail.com',
        packages=find_packages(include='data_manager.*'),
        package_data={
            'data_manager': ['examples/*'],
        },
        long_description=long_description,
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python',
            'Topic :: Utilities',
        ],
        url='https://github.com/abhirupmishra/data_manager',
        install_requires=install_reqs,
        extras_require=extra_reqs,
    )
