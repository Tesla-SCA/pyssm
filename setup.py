from setuptools import setup, find_packages

setup(
    name='pyssm',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/Tesla-SCA/pyssm',
    license='',
    author='Landon Mossburg',
    author_email='lmossburg@tesla.com',
    description='Provides a simple wrapper for getting, working with, and refreshing ssm_params',
    install_requires=["boto3"]
)
