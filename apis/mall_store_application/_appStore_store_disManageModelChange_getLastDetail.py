import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_disManageModelChange_getLastDetail(params=params, headers=headers):
    """
    获取最新的申请记录
    /appStore/store/disManageModelChange/getLastDetail

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/store/disManageModelChange/getLastDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
