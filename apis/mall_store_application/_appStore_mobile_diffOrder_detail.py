import os

from util.client import client

params = {
    "orderId": 0,  # orderId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_diffOrder_detail(params=params, headers=headers):
    """
    货损货差单详情
    /appStore/mobile/diffOrder/detail

    参数说明:
    - orderId: orderId
    """

    url = "/appStore/mobile/diffOrder/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
