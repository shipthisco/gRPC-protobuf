import os
import sys
from fnmatch import fnmatch

# Set a default version
DEFAULT_VERSION = '1.1.8'

# Get the version from command-line arguments or use the default
if len(sys.argv) < 2:
    VERSION = DEFAULT_VERSION
else:
    VERSION = sys.argv[1]
    
dist_folder = 'pyshipproto'

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the 'protobuf' folder
package_folder = os.path.join(current_dir, '..', '..', 'protobuf')

# Create the dist_folder if it doesn't exist
pyshipproto_path = os.path.join(current_dir, dist_folder)
if not os.path.isdir(pyshipproto_path):
    os.mkdir(pyshipproto_path)

# Gather all .proto files in the protobuf directory
proto_files = [os.path.join(path, name) for path, subdirs, files in os.walk(package_folder) for name in files if fnmatch(name, '*.proto')]

# List to keep track of generated proto module names
proto_module_names = []

for proto_file_path in proto_files:
    proto_file_name = os.path.basename(proto_file_path).replace('.proto', '')
    
    # Compile the .proto file
    command = f'python3 -m grpc_tools.protoc -I{package_folder} --python_out={pyshipproto_path} --grpc_python_out={pyshipproto_path} {proto_file_path}'
    os.system(command)

    # Create __init__.py file in the proto_file_name directory
    proto_package_path = os.path.join(pyshipproto_path, proto_file_name)
    if not os.path.isdir(proto_package_path):
        os.mkdir(proto_package_path)
    
    init_file_path = os.path.join(proto_package_path, '__init__.py')
    with open(init_file_path, 'w') as init_file:
        init_file.write(f'from . import {proto_file_name}_pb2\n')
        init_file.write(f'from . import {proto_file_name}_pb2_grpc\n')
    
    # Store the module name for the overall __init__.py
    proto_module_names.append(proto_file_name)

    # Update the generated _pb2_grpc.py file
    grpc_file_path = os.path.join(pyshipproto_path, f'{proto_file_name}/{proto_file_name}_pb2_grpc.py')
    if os.path.exists(grpc_file_path):
        with open(grpc_file_path, 'r') as grpc_file:
            grpc_content = grpc_file.readlines()
        
        # Replace the line in the grpc file
        new_content = []
        for line in grpc_content:
            if line.startswith(f'from {proto_file_name} import {proto_file_name}_pb2 as {proto_file_name}_dot_{proto_file_name}__pb2'):
                new_line = line.replace(f'from {proto_file_name} import {proto_file_name}_pb2 as {proto_file_name}_dot_{proto_file_name}__pb2', 
                                        f'from . import {proto_file_name}_pb2 as {proto_file_name}_dot_{proto_file_name}__pb2')
                new_content.append(new_line)
            else:
                new_content.append(line)

        # Write the modified content back to the file
        with open(grpc_file_path, 'w') as grpc_file:
            grpc_file.writelines(new_content)

# Create a single __init__.py in the dist_folder to import all modules
main_init_file_path = os.path.join(pyshipproto_path, '__init__.py')
with open(main_init_file_path, 'w') as main_init_file:
    main_init_file.write(f'from . import *\n')  # Import all proto modules

# Create a single setup.py for the pyshipproto folder
setup_file_content = f"""
from setuptools import setup, find_packages

VERSION = '{VERSION}' 
DESCRIPTION = 'PyShipProto Package'
LONG_DESCRIPTION = 'Pyshipproto package with generated gRPC services.'

# Setting up
setup(
    name="pyshipproto",
    version=VERSION,
    author="PyShipProto",
    author_email="<pyshipproto@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/shipthisco/gRPC-protobuf",
    install_requires=[],
    keywords=['python', 'gRPC', 'protobuf', 'pyshipproto'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
"""

# Specify the path for setup.py to be in the same directory as the scripts
setup_file_path = os.path.join(current_dir, 'setup.py')
with open(setup_file_path, 'w') as setup_file:
    setup_file.write(setup_file_content)

# Run the build command for the pyshipproto package
build_command = f'python3 {setup_file_path} sdist bdist_wheel'
os.system(build_command)
