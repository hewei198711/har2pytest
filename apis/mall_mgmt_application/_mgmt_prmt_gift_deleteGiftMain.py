import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_gift_deleteGiftMain(data=data, headers=headers):
    """
    删除赠品派发任务
    /mgmt/prmt/gift/deleteGiftMain

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/gift/deleteGiftMain"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
