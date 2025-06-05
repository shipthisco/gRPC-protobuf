# 🚢 Shipthis gRPC Protobufs

Welcome to the collection of protobuf definitions used across Shipthis services. These files generate language specific libraries for seamless communication between microservices.

## 📂 Repository layout

- **protobuf/** – Source `.proto` files defining gRPC services
- **go/** – Generated Go bindings
- **scripts/** – Helpers to build Python and JavaScript packages

## 📦 Installation

### JavaScript
```bash
npm install jsshipproto
```

### Python
```bash
pip install git+https://github.com/shipthisco/gRPC-protobuf.git
```

## 🛠️ Building from source

To generate the JavaScript package locally, ensure `grpc_tools_node_protoc` is available globally or let the script fetch it with `npx`:

```bash
npm install -g grpc-tools # optional
node scripts/javascript/generate_lib.js <version>
# The script will use `npx -p grpc-tools` automatically if the tool isn't installed.
```

For Python packages run:

```bash
python scripts/python/generate_lib.py <version>
```

## ✨ Supported services

- Authentication
- Generic CRUD operations
- Code execution

## 🤝 Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## 📜 License

This project is licensed under the [MIT License](LICENSE).
