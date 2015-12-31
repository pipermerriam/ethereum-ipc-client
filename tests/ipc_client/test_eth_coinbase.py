import os

from eth_ipc_client import Client


BASE_DIR = os.path.dirname(__file__)
project_dir = os.path.join(BASE_DIR, 'project-01')


def test_get_coinbase(ipc_client):
    cb = ipc_client.get_coinbase()

    assert cb == '0x82a978b3f5962a5b0957d9ee9eef472ee55b42f1'
