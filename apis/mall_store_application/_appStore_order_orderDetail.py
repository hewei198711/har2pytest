import os

from util.client import client

params = {
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderDetail(params=params, headers=headers):
    """
    订单详情
    /appStore/order/orderDetail

    参数说明:
    - orderNo: orderNo
    """

    url = "/appStore/order/orderDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
