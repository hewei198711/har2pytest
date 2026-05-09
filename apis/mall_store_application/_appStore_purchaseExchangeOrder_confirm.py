import os

from util.client import client

data = {
    "id": 0,  # 换货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseExchangeOrder_confirm(data=data, headers=headers):
    """
    确认收货
    /appStore/purchaseExchangeOrder/confirm

    参数说明:
    - id: 换货单id
    """

    url = "/appStore/purchaseExchangeOrder/confirm"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
