import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_disManageModelChange_getIsCancel(params=params, headers=headers):
    """
    查询服务中心是否已取消资格:已取消资格返回true
    /appStore/store/disManageModelChange/getIsCancel

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/store/disManageModelChange/getIsCancel"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
