#!/bin/bash

python -m grpc_tools.protoc -I . --python_out=api --grpc_python_out=api api.proto
python server.py
