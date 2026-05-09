import os

from util.client import client

params = {
    "signNo": "",  # signNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderSign_cancelSign(params=params, headers=headers):
    """
    取消签约购
    /appStore/order/orderSign/cancelSign

    参数说明:
    - signNo: signNo
    """

    url = "/appStore/order/orderSign/cancelSign"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
