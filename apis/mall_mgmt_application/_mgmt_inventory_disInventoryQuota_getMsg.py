import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryQuota_getMsg(params=params, headers=headers):
    """
    获取库存限额信息
    /mgmt/inventory/disInventoryQuota/getMsg

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/disInventoryQuota/getMsg"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
