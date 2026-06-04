import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_getOrdersCountForMonth(params=params, headers=headers):
    """
    getOrdersCountForMonth
    /mgmt/inventory/order/getOrdersCountForMonth

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/order/getOrdersCountForMonth"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
