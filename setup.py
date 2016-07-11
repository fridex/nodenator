#!/usr/bin/python

from nodenator.version import nodenator_version
from setuptools import setup, find_packages

# Note: We are not distributing examples/ for now


def get_requirements():
    with open('requirements.txt') as fd:
        return fd.read().splitlines()


setup(
    name='nodenator',
    version=nodenator_version,
    packages=find_packages(),
    scripts=['nodenator-cli'],
    install_requires=get_requirements(),
    author='Fridolin Pokorny',
    author_email='fpokorny@redhat.com',
    maintainer='Fridolin Pokorny',
    maintainer_email='fpokorny@redhat.com',
    description='A node Python code generator and evaluator',
    url='https://github.com/fridex/nodenator',
    license='GPL',
    keywords='petrinet node task graph edge',
)
