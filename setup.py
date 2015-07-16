# -*- coding: utf-8 -*-
# Doc - http://flask.pocoo.org/docs/0.10/patterns/distribute/
import os
from setuptools import setup, find_packages


def get_build_number():
    ci_build_env = {
        "Codeship": "CI_BUILD_NUMBER",
        "Jenkins": "BUILD_NUMBER"
    }
    for ci_env in ci_build_env.values():
        if ci_env in os.environ:
            return os.environ[ci_env]
    return "0000"

setup(
    name="dcsqa-sample-service",
    version='0.1' + "-" + get_build_number(),
    url='',
    description='DCS QA Sample Service',
    author='Trend Micro DCS-RD Team',
    author_email='dcsrd@dl.trendmicro.com',
    packages=find_packages(exclude=("tests", "tests.*", "bin", "bin.*")),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=0.10.1',
        'boto3>=1.1.0',
        'mock>=1.1.2',
        'Flask-API>=0.6.3',
        'Flask-HTTPAuth'
    ],
)
