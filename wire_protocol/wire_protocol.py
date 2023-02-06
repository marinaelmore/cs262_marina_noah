import re


# requests take the form (COMMAND, ARG0, ARG1...)
# they are serialized as COMMAND:ARG0:ARG1:...:EOM
# responses take the form <String>
class WireProtocol:

    # create regexes for each command in the protocol
    create_protocol = re.compile(
        "^(CREATE):([a-zA-Z0-9]+):EOM$", re.IGNORECASE)
    login_protocol = re.compile("^(LOGIN):([a-zA-Z0-9]+):EOM$", re.IGNORECASE)
    list_protocol = re.compile("^(LIST):(.*):EOM$", re.IGNORECASE)
    send_protocol = re.compile(
        "^(SEND):([a-zA-Z0-9]+):(.+):EOM$", re.IGNORECASE)
    delete_protocol = re.compile(
        "^(DELETE):([a-zA-Z0-9]+):EOM$", re.IGNORECASE)

    protocol_list = [create_protocol, login_protocol,
                     send_protocol, list_protocol, send_protocol, delete_protocol]

    MAX_BYTES = 2000
    COMMANDS = ["CREATE", "LOGIN", "SEND", "LIST", "DELETE"]

    def serialize_request(command, *body):
        if command not in WireProtocol.COMMANDS:
            raise ValueError("Invalid command")
        formatted = ""
        if command == "CREATE":
            formatted = "CREATE:{}:EOM".format(body[0])
        if command == "LOGIN":
            formatted = "LOGIN:{}:EOM".format(body[0])
        if command == "SEND":
            formatted = "SEND:{}:{}:EOM".format(body[0], body[1])
        if command == "LIST":
            formatted = "LIST:{}:EOM".format(body[0])
        if command == "DELETE":
            formatted = "DELETE:{}:EOM".format(body[0])
        encoded = formatted.encode()
        if (len(encoded) > WireProtocol.MAX_BYTES):
            raise ValueError("Message too long")
        return encoded

    def deserialize_request(data):
        test = data.decode()
        print("TEST", test)
        for protocol in WireProtocol.protocol_list:
            match = protocol.match(test)
            if match:
                print("MATCH", match.groups())
                return match.groups()
        return None
