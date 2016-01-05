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
        self._socket = self.get_socket()

        super(Client, self).__init__(*args, **kwargs)

    def get_socket(self):
        _socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        _socket.connect(self.ipc_path)
        # Tell the socket not to block on reads.
        _socket.settimeout(2)
        return _socket

    def _make_request(self, method, params):
        request = self.construct_json_request(method, params)

        for _ in range(3):
            self._socket.sendall(request)
            response_raw = ""

            while True:
                try:
                    response_raw += self._socket.recv(4096)
                except socket.timeout:
                    break

            if response_raw == "":
                self._socket.close()
                self._socket = self.get_socket()
                continue

            break
        else:
            raise ValueError("No JSON returned by socket")

        response = json.loads(response_raw)

        if "error" in response:
            raise ValueError(response["error"]["message"])

        return response
