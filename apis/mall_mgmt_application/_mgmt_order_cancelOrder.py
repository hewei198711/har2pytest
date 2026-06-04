import os
from urllib.parse import urlencode

from util.client import client

data = {
    "remarks": "",  # remarks
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_order_cancelOrder(data=data, headers=headers):
    """
    取消订单
    /mgmt/order/cancelOrder

    参数说明:
    - remarks: remarks
    """

    url = "/mgmt/order/cancelOrder"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
