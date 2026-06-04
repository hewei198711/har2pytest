import os

from util.client import client

params = {
    "orderId": 0,  # orderId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_exchangeOrder_exchangeOrderDetail(params=params, headers=headers):
    """
    后台押货换货单详情
    /mgmt/inventory/exchangeOrder/exchangeOrderDetail

    参数说明:
    - orderId: orderId
    """

    url = "/mgmt/inventory/exchangeOrder/exchangeOrderDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
