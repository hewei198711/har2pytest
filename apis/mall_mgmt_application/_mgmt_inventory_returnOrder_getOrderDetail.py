import os

from util.client import client

params = {
    "orderId": 0,  # orderId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_returnOrder_getOrderDetail(params=params, headers=headers):
    """
    后台押货退货单详情
    /mgmt/inventory/returnOrder/getOrderDetail

    参数说明:
    - orderId: orderId
    """

    url = "/mgmt/inventory/returnOrder/getOrderDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
