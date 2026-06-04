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


def _mgmt_inventory_dis_mortgage_exchangeOrder_cancel(data=data, headers=headers):
    """
    取消
    /mgmt/inventory/dis/mortgage/exchangeOrder/cancel

    参数说明:
    - cancelRemark: 取消原因
    - orderId: 押货换货单id
    """

    url = "/mgmt/inventory/dis/mortgage/exchangeOrder/cancel"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
