import socket
import json

from eth_client_utils import (
    JSONRPCBaseClient,
)

from .utils import get_default_ipc_path


class Client(JSONRPCBaseClient):
    def __init__(self, ipc_path=None, *args, **kwargs):
        if ipc_path is None:
            ipc_path = get_default_ipc_path()

        self.ipc_path = ipc_path

        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.connect(ipc_path)
        # Tell the socket not to block on reads.
        self.socket.settimeout(1)

        super(Client, self).__init__(*args, **kwargs)

    def _make_request(self, method, params):
        request = self.construct_json_request(method, params)
        self.socket.sendall(request)
        response_raw = ""

        while True:
            try:
                response_raw += self.socket.recv(4096)
            except socket.timeout:
                break

        response = json.loads(response_raw)

        if "error" in response:
            raise ValueError(response["error"]["message"])

        return response
