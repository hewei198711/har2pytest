import os

from util.client import client

params = {
    "orderId": 0,  # orderId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_getOrderDetail(params=params, headers=headers):
    """
    后台获取押货单详情
    /mgmt/inventory/order/getOrderDetail

    参数说明:
    - orderId: orderId
    """

    url = "/mgmt/inventory/order/getOrderDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
