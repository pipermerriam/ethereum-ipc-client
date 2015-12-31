import os
import socket
import json
import numbers

class Client(object):
    _nonce = 0

    def __init__(self, ipc_path=None):
        if ipc_path is None:
            ipc_path = os.path.expanduser("~/Library/Ethereum/geth.ipc")

        self.ipc_path = ipc_path

        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind(ipc_path)


    def get_nonce(self):
        self._nonce += 1
        return self._nonce

    @property
    def default_from_address(self):
        return self.get_coinbase()

    def make_ipc_request(self, method, params):
        request_data = json.dumps({
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self.get_nonce(),
        })
        self.socket.send(request_data)
        response = self.socket.recv(1024)
        import ipdb; ipdb.set_trace()
        response_data = json.loads(response.body)
        return response_data

    def get_coinbase(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_coinbase
        """
        response = self.make_ipc_request("eth_coinbase", [])
        return response['result']
