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


def _mgmt_inventory_returnOrder_deleteOrder(data=data, headers=headers):
    """
    删除已取消的退货单
    /mgmt/inventory/returnOrder/deleteOrder

    参数说明:
    - orderId: orderId
    """

    url = "/mgmt/inventory/returnOrder/deleteOrder"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
