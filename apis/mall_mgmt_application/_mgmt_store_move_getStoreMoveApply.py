import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_move_getStoreMoveApply(params=params, headers=headers):
    """
    根据id查询搬迁申请记录
    /mgmt/store/move/getStoreMoveApply

    参数说明:
    - id: id
    """

    url = "/mgmt/store/move/getStoreMoveApply"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
