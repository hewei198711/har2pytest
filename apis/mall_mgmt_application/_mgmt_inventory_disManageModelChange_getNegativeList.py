import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManageModelChange_getNegativeList(params=params, headers=headers):
    """
    负库存列表
    /mgmt/inventory/disManageModelChange/getNegativeList

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/disManageModelChange/getNegativeList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
