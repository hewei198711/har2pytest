import os

from util.client import client

params = {
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_order_detail(params=params, headers=headers):
    """
    订单详情
    /appStore/mobile/order/detail

    参数说明:
    - orderNo: orderNo
    """

    url = "/appStore/mobile/order/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
