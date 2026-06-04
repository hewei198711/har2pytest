import os

from util.client import client

data = {
    "cancelRemark": "",  # 取消原因
    "orderId": 0,  # 押货换货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_exchangeOrder_cancelOrder(data=data, headers=headers):
    """
    取消处理中的换货单
    /mgmt/inventory/exchangeOrder/cancelOrder

    参数说明:
    - cancelRemark: 取消原因
    - orderId: 押货换货单id
    """

    url = "/mgmt/inventory/exchangeOrder/cancelOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
