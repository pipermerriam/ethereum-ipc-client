import os
import sys


def get_default_ipc_path():
    if sys.platform == 'darwin':
        ipc_path = os.path.expanduser("~/Library/Ethereum/geth.ipc")
    elif sys.platform == 'linux2':
        ipc_path = os.path.expanduser("~/.ethereum/geth.ipc")
    elif sys.platform == 'win32':
        ipc_path = os.path.expanduser("\\~\\AppData\\Roaming\\Ethereum")
    else:
        raise ValueError(
            "Unsupported platform.  Only darwin/linux2/win32 are "
            "supported.  You must specify the ipc_path"
        )
    return ipc_path
