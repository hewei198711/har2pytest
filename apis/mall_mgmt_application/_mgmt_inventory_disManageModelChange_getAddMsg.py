import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManageModelChange_getAddMsg(params=params, headers=headers):
    """
    获取新增所需信息
    /mgmt/inventory/disManageModelChange/getAddMsg

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/disManageModelChange/getAddMsg"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
