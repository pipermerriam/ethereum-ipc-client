import os
import pytest


BASE_DIR = os.path.dirname(__file__)
geth_project_dir = os.path.join(BASE_DIR, 'project-01')


@pytest.fixture(autouse=True)
def _geth_node(geth_node):
    return geth_node



def test_send_a_transaction(ipc_client, geth_coinbase, geth_accounts):
    to_addr = geth_accounts[1]

    before_balance = ipc_client.get_balance(to_addr)

    txn_hash = ipc_client.send_transaction(
        _from=geth_coinbase,
        to=to_addr,
        value=12345,
    )
    txn_receipt = ipc_client.wait_for_transaction(txn_hash)

    after_balance = ipc_client.get_balance(to_addr)

    assert after_balance - before_balance == 12345


def test_send_a_transaction_defaults_to_coinbase_as_from(ipc_client,
                                                         geth_coinbase,
                                                         geth_accounts):
    to_addr = geth_accounts[1]

    before_balance = ipc_client.get_balance(to_addr)

    txn_hash = ipc_client.send_transaction(
        to=to_addr,
        value=12345,
    )
    txn_receipt = ipc_client.wait_for_transaction(txn_hash)

    after_balance = ipc_client.get_balance(to_addr)

    assert after_balance - before_balance == 12345


def test_contract_creation(ipc_client, geth_coinbase):
    data = "0x60606040525b5b600a8060136000396000f30060606040526008565b00"

    txn_hash = ipc_client.send_transaction(
        _from=geth_coinbase,
        value=12345,
        data=data,
    )
    txn_receipt = ipc_client.wait_for_transaction(txn_hash)
    contract_addr = txn_receipt['contractAddress']

    contract_balance = ipc_client.get_balance(contract_addr)
    assert contract_balance == 12345
