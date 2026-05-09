import os

from util.client import client

data = {
    "id": 0,  # 换货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseExchangeOrder_cancel(data=data, headers=headers):
    """
    取消待审核或待退回的换货单
    /appStore/purchaseExchangeOrder/cancel

    参数说明:
    - id: 换货单id
    """

    url = "/appStore/purchaseExchangeOrder/cancel"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
