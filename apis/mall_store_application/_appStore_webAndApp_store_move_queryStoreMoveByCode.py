import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_webAndApp_store_move_queryStoreMoveByCode(params=params, headers=headers):
    """
    根据storeCode查询最新搬迁记录
    /appStore/webAndApp/store/move/queryStoreMoveByCode

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/webAndApp/store/move/queryStoreMoveByCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
