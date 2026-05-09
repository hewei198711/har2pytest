import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_inventoryCheck_finishCheck(headers=headers):
    """
    完成盘点
    /appStore/inventoryCheck/finishCheck
    """

    url = "/appStore/inventoryCheck/finishCheck"
    with client.post(url=url, headers=headers) as r:
        return r
