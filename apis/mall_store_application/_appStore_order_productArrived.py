import os

from util.client import client

data = {
    "orderNo": "",  # 产品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_productArrived(data=data, headers=headers):
    """
    商品已到店
    /appStore/order/productArrived

    参数说明:
    - orderNo: 产品编码
    """

    url = "/appStore/order/productArrived"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
