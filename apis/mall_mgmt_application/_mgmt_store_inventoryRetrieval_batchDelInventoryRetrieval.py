import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_inventoryRetrieval_batchDelInventoryRetrieval(headers=headers):
    """
    批量删除库存检索
    /mgmt/store/inventoryRetrieval/batchDelInventoryRetrieval
    """

    url = "/mgmt/store/inventoryRetrieval/batchDelInventoryRetrieval"
    with client.post(url=url, headers=headers) as r:
        return r
