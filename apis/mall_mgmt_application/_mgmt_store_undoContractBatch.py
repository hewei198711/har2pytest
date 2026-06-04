import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_undoContractBatch(headers=headers):
    """
    批量撤销合同
    /mgmt/store/undoContractBatch
    """

    url = "/mgmt/store/undoContractBatch"
    with client.post(url=url, headers=headers) as r:
        return r
