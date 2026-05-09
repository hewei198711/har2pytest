import os

from util.client import client

params = {
    "orderId": 0,  # orderId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_productDiff_detail(params=params, headers=headers):
    """
    获取货损货差单详情
    /appStore/productDiff/detail

    参数说明:
    - orderId: orderId
    """

    url = "/appStore/productDiff/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
