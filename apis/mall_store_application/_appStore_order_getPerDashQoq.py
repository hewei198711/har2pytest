import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_getPerDashQoq(headers=headers):
    """
    业绩看板-服务中心交付业绩环比图
    /appStore/order/getPerDashQoq
    """

    url = "/appStore/order/getPerDashQoq"
    with client.get(url=url, headers=headers) as r:
        return r
