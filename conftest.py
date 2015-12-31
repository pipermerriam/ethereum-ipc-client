import os

import pytest


@pytest.fixture()
def geth_data_dir(populus_config):
    from populus.geth import get_geth_data_dir

    data_dir = get_geth_data_dir(populus_config.project_dir, populus_config.geth_chain_name)
    return data_dir


@pytest.fixture()
def ipc_client(geth_data_dir):
    from eth_ipc_client import Client

    ipc_path = os.path.join(geth_data_dir, 'geth.ipc')
    client = Client(ipc_path)
    return client
