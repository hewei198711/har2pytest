import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_disInventoryTransfer_getLastRecord(params=params, headers=headers):
    """
    根据服务中心查询最新库存转移记录
    /appStore/store/disInventoryTransfer/getLastRecord

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/store/disInventoryTransfer/getLastRecord"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
