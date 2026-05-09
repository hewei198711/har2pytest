import os

from util.client import client

data = {
    "cancelReason": "",  # 取消原因
    "id": 0,  # 退货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseReturnOrder_cancel(data=data, headers=headers):
    """
    退货单取消
    /appStore/purchaseReturnOrder/cancel

    参数说明:
    - cancelReason: 取消原因
    - id: 退货单id
    """

    url = "/appStore/purchaseReturnOrder/cancel"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
