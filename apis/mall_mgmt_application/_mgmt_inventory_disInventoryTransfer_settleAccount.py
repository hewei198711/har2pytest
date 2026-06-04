import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryTransfer_settleAccount(params=params, headers=headers):
    """
    确认结清账务
    /mgmt/inventory/disInventoryTransfer/settleAccount

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/disInventoryTransfer/settleAccount"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
