import os

from util.client import client

params = {
    "orderSn": "",  # orderSn
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_getOrderDetailBySn(params=params, headers=headers):
    """
    后台获取押货单详情
    /mgmt/inventory/order/getOrderDetailBySn

    参数说明:
    - orderSn: orderSn
    """

    url = "/mgmt/inventory/order/getOrderDetailBySn"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
