import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_getStoreDeliverInfo(headers=headers):
    """
    门店管理-配送数据
    /appStore/order/getStoreDeliverInfo
    """

    url = "/appStore/order/getStoreDeliverInfo"
    with client.get(url=url, headers=headers) as r:
        return r
