import os
from urllib.parse import urlencode

from util.client import client

data = {
    "orderId": 0,  # orderId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_purchaseReturnOrder_delete(data=data, headers=headers):
    """
    退货单删除
    /appStore/purchaseReturnOrder/delete

    参数说明:
    - orderId: orderId
    """

    url = "/appStore/purchaseReturnOrder/delete"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
