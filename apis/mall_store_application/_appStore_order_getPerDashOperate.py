import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_getPerDashOperate(headers=headers):
    """
    业绩看板-服务中心及个人运作情况
    /appStore/order/getPerDashOperate
    """

    url = "/appStore/order/getPerDashOperate"
    with client.get(url=url, headers=headers) as r:
        return r
