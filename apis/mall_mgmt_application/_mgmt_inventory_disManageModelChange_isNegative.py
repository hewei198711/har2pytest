import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManageModelChange_isNegative(params=params, headers=headers):
    """
    实时是否存在负库存:存在返回true
    /mgmt/inventory/disManageModelChange/isNegative

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/disManageModelChange/isNegative"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
