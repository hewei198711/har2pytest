import os

from util.client import client

params = {
    "orderId": 0,  # orderId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseExchangeOrder_returnInfo(params=params, headers=headers):
    """
    获取退回信息
    /appStore/purchaseExchangeOrder/returnInfo

    参数说明:
    - orderId: orderId
    """

    url = "/appStore/purchaseExchangeOrder/returnInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
