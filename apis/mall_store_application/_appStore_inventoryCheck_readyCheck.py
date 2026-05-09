import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_inventoryCheck_readyCheck(headers=headers):
    """
    马上盘点
    /appStore/inventoryCheck/readyCheck
    """

    url = "/appStore/inventoryCheck/readyCheck"
    with client.post(url=url, headers=headers) as r:
        return r
