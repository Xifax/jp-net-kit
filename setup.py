# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='jpNetKit',
    version='0.1dev',
    author='Artiom Basenko',
    author_email='demi.log@gmail.com',
    packages=['jpnetkit', 'jpnetkit.test'],
    url='http://pypi.python.org/pypi/jp-net-kit/',
    license='LICENSE.txt',
    description='jp2en web services api collection',
    long_description=open('README.txt').read(),
    install_requires=[
        "Requests >= 1.1.0",
        "beautifulsoup4 >= 4.1.3",
        "jcconv   >= 0.2.3",
        "lxml >= 2.3.6",
    ],
)
