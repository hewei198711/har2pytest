import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_inventoryCheck_isStoreFinishChecked(headers=headers):
    """
    店铺是否已完成盘点
    /appStore/inventoryCheck/isStoreFinishChecked
    """

    url = "/appStore/inventoryCheck/isStoreFinishChecked"
    with client.get(url=url, headers=headers) as r:
        return r
