import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryTransfer_getPermissionAndAmount(params=params, headers=headers):
    """
    根据storeCode查询权限和当前押货余额
    /mgmt/inventory/disInventoryTransfer/getPermissionAndAmount

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/disInventoryTransfer/getPermissionAndAmount"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
