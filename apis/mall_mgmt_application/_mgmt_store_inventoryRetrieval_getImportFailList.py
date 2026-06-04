import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_inventoryRetrieval_getImportFailList(headers=headers):
    """
    获取导入库存检索败列表
    /mgmt/store/inventoryRetrieval/getImportFailList
    """

    url = "/mgmt/store/inventoryRetrieval/getImportFailList"
    with client.get(url=url, headers=headers) as r:
        return r
