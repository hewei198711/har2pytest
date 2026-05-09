import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_getDiscountOrderCount(headers=headers):
    """
    85折订单金额pv统计
    /appStore/order/getDiscountOrderCount
    """

    url = "/appStore/order/getDiscountOrderCount"
    with client.get(url=url, headers=headers) as r:
        return r
