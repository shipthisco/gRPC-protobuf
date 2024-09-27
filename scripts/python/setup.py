from setuptools import setup, find_packages
import os
print(find_packages())

version = "V1.1.2"
if version:
    setup(
        name = 'pyshipproto', 
        version=version, 
        packages=find_packages(),
        url="https://github.com/shipthisco/gRPC-protobuf"
    )
