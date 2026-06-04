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


def _mgmt_inventory_returnOrder_cancelOrder(data=data, headers=headers):
    """
    取消未审核的退货单
    /mgmt/inventory/returnOrder/cancelOrder

    参数说明:
    - cancelReason: 取消原因
    - id: 退货单id
    """

    url = "/mgmt/inventory/returnOrder/cancelOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
