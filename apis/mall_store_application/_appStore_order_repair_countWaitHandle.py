import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_repair_countWaitHandle(headers=headers):
    """
    统计待处理的维修单
    /appStore/order/repair/countWaitHandle
    """

    url = "/appStore/order/repair/countWaitHandle"
    with client.get(url=url, headers=headers) as r:
        return r
