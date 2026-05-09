import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_webAndApp_store_move_getStoreMoveApply(params=params, headers=headers):
    """
    根据id查询搬迁申请记录
    /appStore/webAndApp/store/move/getStoreMoveApply

    参数说明:
    - id: id
    """

    url = "/appStore/webAndApp/store/move/getStoreMoveApply"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
