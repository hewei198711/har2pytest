import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryTransfer_getDeposit(params=params, headers=headers):
    """
    根据storeCode查询保证金
    /mgmt/inventory/disInventoryTransfer/getDeposit

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/disInventoryTransfer/getDeposit"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
