import os

import pytest



BASE_DIR = os.path.dirname(__file__)
geth_project_dir = os.path.join(BASE_DIR, 'project-01')


@pytest.fixture(autouse=True)
def _geth_node(geth_node):
    return geth_node


def test_get_accounts(ipc_client, geth_data_dir, geth_coinbase, geth_accounts):
    accounts = ipc_client.get_accounts()

    assert len(accounts) > 0
    assert geth_coinbase in accounts
    assert set(accounts) == set(geth_accounts)


def test_get_balance(ipc_client, geth_coinbase):
    balance = ipc_client.get_balance(geth_coinbase)

    assert balance == 1000000000000000000000000000


def test_get_block_by_hash(ipc_client, geth_coinbase):
    txn_hash = ipc_client.send_transaction(_from=geth_coinbase, to=geth_coinbase, value=1)
    txn_receipt = ipc_client.wait_for_transaction(txn_hash)

    block_hash = txn_receipt['blockHash']

    block = ipc_client.get_block_by_hash(block_hash)
    assert block


def test_get_block_number(ipc_client, geth_coinbase, geth_accounts):
    initial_block_number = ipc_client.get_block_number()

    to_addr = geth_accounts[1]
    txn_hash = ipc_client.send_transaction(_from=geth_coinbase, to=to_addr, value=100)
    assert txn_hash
    txn_receipt = ipc_client.wait_for_transaction(txn_hash)

    block_number = ipc_client.get_block_number()
    assert block_number > initial_block_number


def test_get_block_by_number(ipc_client, geth_coinbase, geth_accounts):
    to_addr = geth_accounts[1]
    txn_hash = ipc_client.send_transaction(_from=geth_coinbase, to=to_addr, value=100)
    assert txn_hash
    txn_receipt = ipc_client.wait_for_transaction(txn_hash)

    block_number = ipc_client.get_block_number()

    block = ipc_client.get_block_by_number(int(txn_receipt['blockNumber'], 16))
    assert block


def test_get_code(ipc_client, geth_coinbase):
    data = "0x606060405260f8806100126000396000f30060606040526000357c01000000000000000000000000000000000000000000000000000000009004806316216f3914604b578063a5f3c23b14606a578063dcf537b1146095576049565b005b605460045060e6565b6040518082815260200191505060405180910390f35b607f60048035906020018035906020015060ba565b6040518082815260200191505060405180910390f35b60a460048035906020015060d0565b6040518082815260200191505060405180910390f35b60008183019050805080905060ca565b92915050565b6000600782029050805080905060e1565b919050565b6000600d9050805080905060f5565b9056"
    txn_hash = ipc_client.send_transaction(
        _from=geth_coinbase,
        data=data,
    )
    txn_receipt = ipc_client.wait_for_transaction(txn_hash)
    contract_addr = txn_receipt['contractAddress']

    code = ipc_client.get_code(contract_addr)
    # TODO: figure out what's going on here and why the two are almost the same
    # but not exactly the same.
    assert len(code) > 100
    assert data.endswith(code[2:])


def test_get_transaction_by_hash(ipc_client, geth_coinbase, geth_accounts):
    to_addr = geth_accounts[1]

    txn_hash = ipc_client.send_transaction(
        _from=geth_coinbase,
        to=to_addr,
        value=12345,
    )

    txn = ipc_client.get_transaction_by_hash(txn_hash)

    assert txn['from'].endswith(geth_coinbase)
    assert txn['to'].endswith(to_addr)
    assert int(txn['value'], 16) == 12345
