import glob
import os
from fnmatch import fnmatch
dist_folder = 'pyshipproto'
package_folder = 'protobuf'

if not os.path.isdir(dist_folder):
    os.mkdir(dist_folder)

proto_files = [ os.path.join(path, name) for path, subdirs, files in os.walk(package_folder)  for name in files if fnmatch(name, '*.proto')]

for proto_file_path in proto_files:
    proto_file = proto_file_path[proto_file_path.rfind('/')+1:].replace('.proto', '')
    proto_folder = proto_file_path[:proto_file_path.rfind('/')]
    
    command = 'python3 -m grpc_tools.protoc --proto_path='+package_folder+' '+proto_file_path+' --python_out='+dist_folder+' --grpc_python_out='+dist_folder
    os.system(command)
    init_file = open(dist_folder + '/' +proto_file_path[proto_file_path.find('/')+1:proto_file_path.rfind('/')] + '/__init__.py', 'w+')
    init_file.write('from . import *')
    init_file.close()

    grpc_file = open('pyshipproto/' + proto_file + "/"+proto_file  + '_pb2_grpc.py', 'r+')
    grpc_content = grpc_file.read()
    grpc_content = grpc_content.replace('from ' + proto_file, 'from pyshipproto.' + proto_file)
    grpc_file.truncate(0)
    grpc_file.seek(0)
    grpc_file.write(grpc_content)
    grpc_file.close()


main_package_file = open(dist_folder + '/__init__.py', 'w+')
main_package_file.write('from . import *')
main_package_file.close()




packages = [d for d in os.listdir(package_folder) if os.path.isdir(os.path.join(package_folder, d))]
print("packages", packages)
if not os.path.isdir(dist_folder):
    os.mkdir(dist_folder)
protos = glob.glob('*.proto')
print(protos)
# os.chdir('packages')
for package in packages:
    print('dist folder', dist_folder)
    package_dist = dist_folder + '/'+package
    if not os.path.isdir(package_dist):
        os.mkdir(package_dist)
    print('making path', package_dist)
    
    # go to the package folder
    input_path = 'protobuf/'+package + '/*.proto'
    output_folder = dist_folder + '/'+package

    command = 'python3 -m grpc_tools.protoc --proto_path=. '+input_path+' --python_out='+ output_folder +' --grpc_python_out=' + output_folder
    # generate python files
    # command = 'python3 -m grpc_tools.protoc -I'+package+' --python_out=. --grpc_python_out=. '
    os.system(command)
[ os.path.join(path, name) for path, subdirs, files in os.walk('packages')  for name in files if fnmatch(name, '*.proto')]

py_file_template = """
from setuptools import setup, find_packages
setup(name='{name}',
    version='{version}',
    packages=find_packages())
    """

py_file = open(output_folder +'/setup.py', 'w+')
py_file.write(py_file_template.format(name=package, version='1.1.2'))
py_file.close()


build_command = 'python3 '+ output_folder+ '/setup.py bdist_wheel'
print(build_command)
os.system(build_command)

