from setuptools import setup, find_packages
import os
print(find_packages())

version = os.environ['PROTO_BUF_LIB_VERSION']
if version:
    setup(
        name = 'pyshipproto', 
        version=version, 
        packages=find_packages()
    )
