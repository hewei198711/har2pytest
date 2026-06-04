import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_getOrdersMsgForMonth(params=params, headers=headers):
    """
    getOrdersMsgForMonth
    /mgmt/inventory/order/getOrdersMsgForMonth

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/order/getOrdersMsgForMonth"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
