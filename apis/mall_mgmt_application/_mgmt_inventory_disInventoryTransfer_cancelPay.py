import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryTransfer_cancelPay(params=params, headers=headers):
    """
    取消支付
    /mgmt/inventory/disInventoryTransfer/cancelPay

    参数说明:
    - id: id
    """

    url = "/mgmt/inventory/disInventoryTransfer/cancelPay"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
