def test_get_code(ipc_client, geth_node):
    max_gas = ipc_client.get_max_gas()
    assert max_gas > 0
