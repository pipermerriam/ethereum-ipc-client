import pytest
import threading

from eth_ipc_client import Client


def test_async_requests(ipc_client):
    ipc_client = Client(ipc_client.ipc_path, async=True)

    threads = []

    def spam_block_number():
        for i in range(10):
            try:
                ipc_client.get_block_number()
            except Exception as e:
                pytest.fail(e.message)

    for i in range(3):
        thread = threading.Thread(target=spam_block_number)
        thread.daemon = True
        thread.start()
        threads.append(thread)

    [thread.join() for thread in threads]
