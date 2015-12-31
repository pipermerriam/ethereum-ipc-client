import os

import pytest


@pytest.fixture(scope="module")
def geth_data_dir(request, populus_config):
    from populus.geth import get_geth_data_dir

    project_dir = populus_config.get_value(request, 'geth_project_dir')
    chain_name = populus_config.get_value(request, 'geth_chain_name')
    data_dir = get_geth_data_dir(project_dir, chain_name)

    return data_dir


@pytest.fixture(scope="module")
def ipc_client(geth_data_dir, geth_node):
    from eth_ipc_client import Client

    ipc_path = os.path.join(geth_data_dir, 'geth.ipc')
    client = Client(ipc_path)
    return client


@pytest.fixture(scope="module")
def geth_accounts(geth_data_dir):
    from populus.geth import get_geth_accounts
    accounts = get_geth_accounts(geth_data_dir)
    return accounts
