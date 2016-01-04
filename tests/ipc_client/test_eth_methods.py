import re
import os
import pytest


BASE_DIR = os.path.dirname(__file__)
geth_project_dir = os.path.join(BASE_DIR, 'project-01')


def test_get_coinbase(ipc_client, geth_node, geth_coinbase):
    cb = ipc_client.get_coinbase()

    assert cb == '0xfbac9f38dfe17a158fd23417faad4c8c5724f400'


def is_valid_filter_id(filt_id):
    check = re.compile("0x[\da-fA-F]+")
    m = check.match(filt_id)
    if m:
        return True
    else:
        return False


def test_new_filter(ipc_client, geth_node):
    filt_id = ipc_client.new_filter(from_block=1, to_block=2)

    assert is_valid_filter_id(filt_id)


@pytest.mark.xfail
def test_uninstall_filter(ipc_client, geth_node):
    filt_id = ipc_client.new_filter()

    assert is_valid_filter_id(filt_id)

    resp = ipc_client.uninstall_filter(filt_id)

    assert resp == True


def test_get_filter_changes(ipc_client, geth_node):
    filt_id = ipc_client.new_filter()
    assert is_valid_filter_id(filt_id)

    resp = ipc_client.get_filter_logs(filt_id)
    assert resp == []
