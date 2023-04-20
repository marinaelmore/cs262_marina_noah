INCLUDE=.
OUTPUT=.
PROTO_FILES="pong.proto"

python3 -m grpc_tools.protoc -I$INCLUDE --python_out=$OUTPUT --grpc_python_out=$OUTPUT $PROTO_FILES

