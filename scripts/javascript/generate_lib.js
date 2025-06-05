const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const DEFAULT_VERSION = '1.1.8';
const VERSION = process.argv[2] || DEFAULT_VERSION;

const distFolder = 'jsshipproto';
const currentDir = __dirname;
const packageFolder = path.join(currentDir, '..', '..', 'protobuf');
const distPath = path.join(currentDir, distFolder);

if (!fs.existsSync(distPath)) {
  fs.mkdirSync(distPath);
}

function findProtoc() {
  try {
    execSync('command -v grpc_tools_node_protoc', { stdio: 'ignore' });
    return 'grpc_tools_node_protoc';
  } catch (_) {
    // Explicitly install grpc-tools via npx so the correct binary is used
    return 'npx -p grpc-tools grpc_tools_node_protoc';
  }
}

const PROTOC_CMD = findProtoc();

function gatherProtos(dir) {
  const results = [];
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    const fullPath = path.join(dir, file);
    if (fs.statSync(fullPath).isDirectory()) {
      results.push(...gatherProtos(fullPath));
    } else if (file.endsWith('.proto')) {
      results.push(fullPath);
    }
  });
  return results;
}

const protoFiles = gatherProtos(packageFolder);

protoFiles.forEach(proto => {
  const command = [
    PROTOC_CMD,
    `--js_out=import_style=commonjs,binary:${distPath}`,
    `--grpc_out=${distPath}`,
    `-I${packageFolder}`,
    proto
  ].join(' ');
  execSync(command, { stdio: 'inherit' });
});

const exportsLines = protoFiles.map(p => {
  const name = path.basename(p, '.proto');
  return `exports.${name} = require('./${name}_pb');`;
});
fs.writeFileSync(path.join(distPath, 'index.js'), exportsLines.join('\n'));

const packageJson = {
  name: 'jsshipproto',
  version: VERSION,
  description: 'JsShipProto package with generated gRPC services.',
  main: 'index.js',
  keywords: ['javascript', 'gRPC', 'protobuf', 'jsshipproto'],
  author: 'JsShipProto',
  license: 'ISC',
};
fs.writeFileSync(
  path.join(distPath, 'package.json'),
  JSON.stringify(packageJson, null, 2)
);

execSync(`npm pack ${distPath}`, { stdio: 'inherit' });

