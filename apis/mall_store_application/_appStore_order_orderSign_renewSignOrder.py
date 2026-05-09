import os

from util.client import client

data = {
    "signNo": "",  # 签约单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderSign_renewSignOrder(data=data, headers=headers):
    """
    继续参与-重新生成签约购订单
    /appStore/order/orderSign/renewSignOrder

    参数说明:
    - signNo: 签约单号
    """

    url = "/appStore/order/orderSign/renewSignOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
