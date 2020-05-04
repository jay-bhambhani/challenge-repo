from setuptools import setup
from pip._internal.req import parse_requirements


install_reqs = parse_requirements('requirements.txt', session='hack')
setup(
    name='s3-stats',
    version='0.0.1',
    install_requires=[str(ir.req) for ir in install_reqs],
    packages=['src']
)