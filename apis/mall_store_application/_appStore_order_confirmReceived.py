import os

from util.client import client

data = {
    "orderNo": "",  # 产品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_confirmReceived(data=data, headers=headers):
    """
    顾客已取货
    /appStore/order/confirmReceived

    参数说明:
    - orderNo: 产品编码
    """

    url = "/appStore/order/confirmReceived"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
