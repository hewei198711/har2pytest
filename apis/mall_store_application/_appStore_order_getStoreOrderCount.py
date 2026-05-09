import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_getStoreOrderCount(headers=headers):
    """
    门店管理-数据简报
    /appStore/order/getStoreOrderCount
    """

    url = "/appStore/order/getStoreOrderCount"
    with client.get(url=url, headers=headers) as r:
        return r
