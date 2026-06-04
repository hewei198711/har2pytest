import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_inventoryRetrieval_importList(headers=headers):
    """
    批量导入库存检索
    /mgmt/store/inventoryRetrieval/importList
    """

    url = "/mgmt/store/inventoryRetrieval/importList"
    with client.post(url=url, headers=headers) as r:
        return r
