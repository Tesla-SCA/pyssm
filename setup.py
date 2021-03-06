from setuptools import setup

setup(
    name='pyssm-sca',
    version='0.2.5',
    py_modules=["pyssm"],
    url='https://github.com/Tesla-SCA/pyssm',
    license='',
    author='Landon Mossburg',
    author_email='lmossburg@tesla.com',
    description='Provides a simple wrapper for getting, working with, and refreshing ssm_params',
    install_requires=["boto3"],
    download_url = 'https://github.com/Tesla-SCA/pyssm/archive/0.1.tar.gz', 
)
