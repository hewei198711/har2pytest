import os

from util.client import client

params = {
    "orderId": 0,  # orderId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_diffOrder_orderDetail(params=params, headers=headers):
    """
    货损货差详情
    /mgmt/inventory/diffOrder/orderDetail

    参数说明:
    - orderId: orderId
    """

    url = "/mgmt/inventory/diffOrder/orderDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
