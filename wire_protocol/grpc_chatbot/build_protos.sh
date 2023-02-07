INCLUDE=.
OUTPUT=.
PROTO_FILES="chatbot.proto"

python -m grpc_tools.protoc -I$INCLUDE --python_out=$OUTPUT --grpc_python_out=$OUTPUT $PROTO_FILES

