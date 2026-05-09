import os

from util.client import client

data = {
    "orderSn": "",  # 押货单编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseOrder_confirm(data=data, headers=headers):
    """
    已发货的押货单确认收货
    /appStore/purchaseOrder/confirm

    参数说明:
    - orderSn: 押货单编号
    """

    url = "/appStore/purchaseOrder/confirm"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
