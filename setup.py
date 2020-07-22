#!/usr/bin/env python
import io
from os import path

from setuptools import setup, find_packages


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return io.open(file_path).read()


setup(
    name='django-polymorphic-foreignkey',
    version='1.1.0',
    license='BSD',
    description='A polymorphic ForeignKey field that acts like a generic ForeignKey',
    long_description=read('README.rst'),
    url='https://github.com/theatlantic/django-polymorphic-foreignkey',
    author='Frankie Dintino',
    author_email='fdintino@theatlantic.com',
    maintainer='The Atlantic',
    maintainer_email='programmers@theatlantic.com',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    zip_safe=False,
    install_requires=[
        'Django>=1.11',
        'python-monkey-business',
        'django-polymorphic',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])
