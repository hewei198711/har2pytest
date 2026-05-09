import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_webAndApp_store_move(params=params, headers=headers):
    """
    根据storeCode查询店铺当前地址
    /appStore/webAndApp/store/move

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/webAndApp/store/move"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
