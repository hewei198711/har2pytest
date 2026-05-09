import os

from util.client import client

params = {
    "orderId": 0,  # orderId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseReturnOrder_detailInfo(params=params, headers=headers):
    """
    获取退货单信息
    /appStore/purchaseReturnOrder/detailInfo

    参数说明:
    - orderId: orderId
    """

    url = "/appStore/purchaseReturnOrder/detailInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
