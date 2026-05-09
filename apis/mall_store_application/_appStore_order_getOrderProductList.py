import os

from util.client import client

params = {
    "orderId": 0,  # orderId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_getOrderProductList(params=params, headers=headers):
    """
    产品信息
    /appStore/order/getOrderProductList

    参数说明:
    - orderId: orderId
    """

    url = "/appStore/order/getOrderProductList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
