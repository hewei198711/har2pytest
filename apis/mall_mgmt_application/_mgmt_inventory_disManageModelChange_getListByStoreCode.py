import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManageModelChange_getListByStoreCode(params=params, headers=headers):
    """
    根据storeCode获取申请记录
    /mgmt/inventory/disManageModelChange/getListByStoreCode

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/disManageModelChange/getListByStoreCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
