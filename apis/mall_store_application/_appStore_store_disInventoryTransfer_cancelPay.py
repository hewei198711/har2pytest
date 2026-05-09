import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_disInventoryTransfer_cancelPay(params=params, headers=headers):
    """
    取消支付
    /appStore/store/disInventoryTransfer/cancelPay

    参数说明:
    - id: id
    """

    url = "/appStore/store/disInventoryTransfer/cancelPay"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
