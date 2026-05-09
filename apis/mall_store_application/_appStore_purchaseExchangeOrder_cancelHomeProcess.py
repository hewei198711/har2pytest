import os

from util.client import client

data = {
    "id": 0,  # 换货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseExchangeOrder_cancelHomeProcess(data=data, headers=headers):
    """
    取消上门取件退回处理
    /appStore/purchaseExchangeOrder/cancelHomeProcess

    参数说明:
    - id: 换货单id
    """

    url = "/appStore/purchaseExchangeOrder/cancelHomeProcess"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
